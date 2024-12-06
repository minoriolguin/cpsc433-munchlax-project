# CPSC 433 - Artificial Intelligence - Fall 2024
# Aditi Yadav
# Jaden Myers
# Minori Olguin
# Monica Nguyen
# Thi Ngoc Anh Nguyen

import signal
import sys
import time
from game import Game
from practice import Practice
from gameSlot import GameSlot
from practiceSlot import PracticeSlot
from input_parser import InputParser
from scheduler import Scheduler
from node import Node
from collections import defaultdict
from hardConstraints import HardConstraints
from softContraints import SoftConstraints

# Global variables
best_schedule = None
best_eval_score = float('inf')
slots = []
pen_gamemin = None
pen_practicemin = None
checked_states = set()
best_schedule_is_complete = False
MAX_DEPTH = 200

# Signal handler to handle early stops
def signal_handler(sig, frame):
    global best_schedule, best_eval_score, slots, softConstraints, best_schedule_is_complete
    if best_schedule:
        status = "Complete" if best_schedule_is_complete else "Partial"
        print(f"\n*Best Schedule Found ({status} - Interrupted): ")
        best_schedule.print_schedule(slots, softConstraints)
    else:
        print("No valid schedule found.")
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# Initialize And-Tree root
def initialize_root(events, game_slots, practice_slots, partial_assign):
    root_schedule = Scheduler(events=events)

    # Check if game slot TU at 11:00 AM is in the file
    # Hard constraint general meeting
    filtered_game_slots = [
        slot for slot in game_slots
        if not (slot.day == "TU" and slot.startTime == "11:00")
    ]

    # Add all other game slots and practices slots valid to be added
    for slot in filtered_game_slots + practice_slots:
        root_schedule.add_slot(slot)

    # check if CMSA U12T1 or CMSA U13T1 requested special practice event
    for event in events:
        if event.id == "CMSA U12T1" or event.id == "CMSA U13T1":
            special_practice_id = f"{event.id}S"
            special_practice_slot = next((slot for slot in practice_slots
                                          if slot.day == "TU" and slot.startTime == "18:00"), None)

            if not special_practice_slot:
                # print(f"Failed to find valid slot for special practice {special_practice_id}.")
                return None

            special_practice = next(
                (e for e in events if e.id == special_practice_id), None)
            if not special_practice:
                # print(f"Special practice {special_practice_id} not found in events.")
                return None

            root_schedule.assign_event(special_practice, special_practice_slot)
            practice_slots.remove(special_practice_slot)

    # assigns any partial assignments for the schedule
    for assign in partial_assign:
        if 'id' not in assign or 'day' not in assign or 'time' not in assign:
            # print(f"Invalid partial assignment format: {assign}")
            return None

        event_id = assign['id']
        day = assign['day'].strip()
        time = assign['time'].strip()

        event = next((e for e in events if e.id == event_id), None)
        if not event:
            # print(f"Event with ID '{event_id}' not found in events.")
            return None

        slot = next((s for s in filtered_game_slots + practice_slots
                     if s.day == day and s.startTime == time), None)
        if not slot:
            return None

        root_schedule.assign_event(event, slot)

    return Node(schedule=root_schedule, sol="?")

# Helper function to sort the events so they aren't random, this also prioritizes the
# evening slots and divisions starting with 9 so they can be places in evening slots first
def reorder_events(events):
    # Group events by league, tier, and division
    grouped = defaultdict(list)
    for event in events:
        team_key = (event.league, event.tier, str(event.div))
        grouped[team_key].append(event)

    # Separate teams with div=9* and others
    div_9_teams = [key for key in grouped if key[2].startswith("9")]
    other_teams = [key for key in grouped if not key[2].startswith("9")]

    # Function to add events for a team (games first, then practices)
    def add_team_events(team_key):
        team_events = grouped[team_key]
        games = [e for e in team_events if isinstance(e, Game)]
        practices = [e for e in team_events if isinstance(e, Practice)]
        return games + practices

    # Reorder events
    reordered_events = []

    # Process div=9* teams
    for team_key in div_9_teams:
        league, tier, _ = team_key
        # Collect all events for the league and tier
        for key in grouped:
            if key[0] == league and key[1] == tier:
                reordered_events.extend(add_team_events(key))

    # Process remaining teams
    for team_key in other_teams:
        league, tier, _ = team_key
        # Collect all events for the league and tier
        for key in grouped:
            if key[0] == league and key[1] == tier:
                reordered_events.extend(add_team_events(key))
                
    return reordered_events

  
def prioritize_slots(event, slots, incompatible_map):
    if isinstance(event, Game):
        valid_slots = [slot for slot in slots if isinstance(slot, GameSlot)]
    elif isinstance(event, Practice):
        valid_slots = [slot for slot in slots if isinstance(slot, PracticeSlot)]
    else:
        return []

    # Filter out incompatible slots
    valid_slots = [
        slot for slot in valid_slots
        if not (hasattr(slot, 'assigned_event') and slot.assigned_event and 
                slot.assigned_event.id in incompatible_map.get(event.id, set()))
    ]

    # Calculate whether the slot meets the game_min constraint
    def meets_game_min(slot):
        if isinstance(slot, GameSlot):
            return slot.remaining_capacity() >= slot.gameMin
        if isinstance(slot, PracticeSlot):
            return slot.remaining_capacity() >= slot.pracMin
        return True 

    prioritized = sorted(
        valid_slots,
        key=lambda slot: (
            event.div != 9,  # False for div 9 (higher priority)
            int(slot.startTime.split(':')[0]) < 18,  # True if start time < 18
            -slot.remaining_capacity(),  # Higher capacity first
            not meets_game_min(slot)  # Prioritize slots that help meet game_min
        )
    )
    return prioritized

# Keep a map of incompatible pairs to use during prioritization
def preprocess_incompatible_pairs(not_compatible):
    incompatible_map = defaultdict(set)
    for pair in not_compatible:
        incompatible_map[pair[0]].add(pair[1])
        incompatible_map[pair[1]].add(pair[0])
    return incompatible_map

# And-Tree build
def build_tree(node, unscheduled_events, parent_slots, check_hard_constraints, softConstraints, incompatible_map, depth=0):
    global best_schedule, best_eval_score, best_schedule_is_complete

    if depth > MAX_DEPTH:
        return

    # Base case: All events scheduled
    if not unscheduled_events:
        # Complete schedule
        eval_score = node.schedule.calculate_eval_value(parent_slots, softConstraints)
        if check_hard_constraints(node.schedule):
            node.sol = "yes"
            if not best_schedule_is_complete or eval_score < best_eval_score:
                best_eval_score = eval_score
                best_schedule = node.schedule.copy_schedule()
                best_schedule_is_complete = True
    else:
        # Partial schedule
        current_eval_score = node.schedule.calculate_eval_value(parent_slots, softConstraints)
        if not best_schedule_is_complete and current_eval_score < best_eval_score:
            best_eval_score = current_eval_score
            best_schedule = node.schedule.copy_schedule()

    # Check for already-visited states
    state_hash = hash(frozenset((slot.id, event.id) for slot, event in node.schedule.scheduleVersion.items() if event != "$"))
    if state_hash in checked_states:
        return
    checked_states.add(state_hash)

    # Reorder events and maintain the order as a flat list
    ordered_events = reorder_events(unscheduled_events)

    for event in ordered_events:
        prioritized_slots = prioritize_slots(event, parent_slots, incompatible_map)

        for slot in prioritized_slots:
            # Skip incompatible slot types
            if isinstance(event, Game) and not isinstance(slot, GameSlot):
                continue
            if isinstance(event, Practice) and not isinstance(slot, PracticeSlot):
                continue

            # Skip full slots
            if slot.is_full():
                continue

            # Create a new node and copy current state
            child_slots = [s.copy() for s in parent_slots]
            new_schedule = node.schedule.copy_schedule()
            new_schedule.assign_event(event, slot)

            # Check the new schedule with hard constraints
            if not check_hard_constraints(new_schedule):
                continue

            # Create a new child node if valid
            child_node = Node(schedule=new_schedule, sol="?")
            node.add_child(child_node)

            # Prune branches with no children
            if not node.children:
                return

            # Continue recursion with remaining events
            remaining_events = [e for e in unscheduled_events if e != event]
            build_tree(child_node, remaining_events, child_slots, check_hard_constraints, softConstraints, incompatible_map, depth + 1)


# Main method
def main():
    parser = InputParser()
    parser.main()

    events = parser.games + parser.practices
    game_slots = parser.gameSlots
    practice_slots = parser.practiceSlots
    partial_assign = parser.partial_assign
    incompatible_map = preprocess_incompatible_pairs(parser.not_compatible)
    
    try:
        root = initialize_root(events, game_slots, practice_slots, partial_assign)
    except ValueError as e:
        print(f"Error initializing root: {e}")
        return None

    unscheduled_events = [event for event in events if not any(assign['id'] == event.id for assign in partial_assign)]
    slots = game_slots + practice_slots
    
    hardConstraints = HardConstraints(parser)
    softConstraints = SoftConstraints(parser)

    try:
        start = time.time()
        build_tree(root, unscheduled_events, slots, hardConstraints.check_hard_constraints, pen_gamemin, pen_practicemin, incompatible_map)
        end = time.time()
    except Exception as e:
        print(f"An error occurred: {e}")
        if best_schedule:
            print("\nBest schedule found before error: \n")
            best_schedule.print_schedule(slots, softConstraints)
        else:
            print("No valid schedule found before error.")
        return 

    elapsed_time_minutes = (end - start) / 60
    print(f"Time to run: {elapsed_time_minutes}")

    if best_schedule:
        print("\nBest schedule found: \n")
        best_schedule.print_schedule(slots, softConstraints)
    else:
        print("No valid schedule found.")

    return root

if __name__ == "__main__":
    root_node = main()
