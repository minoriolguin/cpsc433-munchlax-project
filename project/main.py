# CPSC 433 - Artificial Intelligence - Fall 2024
# Aditi Yadav
# Jaden Myers
# Minori Olguin
# Monica Nguyen
# Thi Ngoc Anh Nguyen

import os
import signal
import sys
import traceback
from game import Game
from practice import Practice
from gameSlot import GameSlot
from practiceSlot import PracticeSlot
from input_parser import InputParser
from scheduler import Scheduler
from node import Node
from collections import defaultdict
from hardConstraints import HardConstraints
from soft_constraints import SoftConstraints

# Global variables
iteration_count = 0
unscheduled_events_count = float('inf')
softConstraints = None
best_schedule = None
best_eval_score = float('inf')
best_schedule_is_complete = False
checked_states = set()
MAX_DEPTH = 500
MAX_ITERATIONS = 100_000

# Signal handler to handle early stops
def signal_handler(sig, frame):
    global best_schedule, best_eval_score, slots, best_schedule_is_complete

    parser = InputParser()
    parser.main()
    if best_schedule:
        status = "Complete" if best_schedule_is_complete else "Partial"
        print(f"\n*Best Schedule Found ({status} - Interrupted): ")
        best_schedule.print_schedule(best_eval_score)
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

            # root_schedule.assign_event(special_practice, special_practice_slot)
            # practice_slots.remove(special_practice_slot)

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
            print(f"Slot with day '{day}' and time '{time}' not found.")
            return None

        root_schedule.assign_event(event, slot)
    
    return Node(schedule=root_schedule, sol="?")

# Helper function to sort the events so they aren't random, this also prioritizes the
# evening slots and divisions starting with 9 so they can be places in evening slots first
def reorder_events(events, incompatible_map, shuffle=False):
    # Group events by league, tier, and division
    grouped = defaultdict(list)
    for event in events:
        team_key = (event.league, event.tier, str(event.div))
        grouped[team_key].append(event)

    # Calculate incompatibility counts for prioritization
    incompatibility_counts = {
        event.id: len(incompatible_map.get(event.id, set())) for event in events
    }

    # Sort teams within each group by their incompatibility count
    def sort_group(team_events):
        return sorted(
            team_events,
            key=lambda e: -incompatibility_counts[e.id]  # More incompatible first
        )

    # Separate teams with div=9* and others
    div_9_teams = [key for key in grouped if key[2].startswith("9")]
    other_teams = [key for key in grouped if not key[2].startswith("9")]

    # Function to add sorted events for a team (games first, then practices)
    def add_team_events(team_key):
        team_events = grouped[team_key]
        games = [e for e in team_events if isinstance(e, Game)]
        practices = [e for e in team_events if isinstance(e, Practice)]
        return sort_group(games) + sort_group(practices)

    # Reorder events
    reordered_events = []

    # Process div=9* teams
    for team_key in div_9_teams:
        league, tier, _ = team_key
        for key in grouped:
            if key[0] == league and key[1] == tier:
                reordered_events.extend(add_team_events(key))

    # Process remaining teams
    for team_key in other_teams:
        league, tier, _ = team_key
        for key in grouped:
            if key[0] == league and key[1] == tier:
                reordered_events.extend(add_team_events(key))

    # Shuffle if enabled
    # if shuffle:
    #     random.shuffle(reordered_events)

    return reordered_events

# Compatibility check function
def check_compatibility(event1, event2, incompatible_map):
    # Check for precomputed incompatibility
    if event1.id in incompatible_map.get(event2.id, set()):
        return False
    if event2.id in incompatible_map.get(event1.id, set()):
        return False
    
    # Add any additional compatibility logic here
    return True

# prioritizes slots based on hard and soft constraints
def prioritize_slots(event, slots, incompatible_map):
    if isinstance(event, Game):
        valid_slots = [slot for slot in slots if isinstance(slot, GameSlot)]
    elif isinstance(event, Practice):
        valid_slots = [slot for slot in slots if isinstance(slot, PracticeSlot)]
    else:
        return []

    # Filter out incompatible slots
    for slot in valid_slots:
        incompatible_events = incompatible_map.get(event.id, set())
        if hasattr(slot, 'assigned_event') and slot.assigned_event:
            assigned_event = slot.assigned_event
            # Perform compatibility check
            if not check_compatibility(event, assigned_event) or assigned_event.id in incompatible_events:
                print(f"DEBUG: Filtering out slot {slot.id} for event {event.id} due to incompatibility with {assigned_event.id}")
                valid_slots.remove(slot)

    # Avoid slots with overlapping divisions within the same tier
    def has_overlapping_division(slot):
        if isinstance(slot, GameSlot):
            current_tier_divisions = [(game.tier, game.div) for game in slot.assignedGames]
            return (event.tier, event.div) in current_tier_divisions  # Check for same tier and division overlap
        return False

    valid_slots = [slot for slot in valid_slots if not has_overlapping_division(slot)]

    # Prioritize based on how far the slot's remaining capacity is from its gameMin
    def distance_from_game_min(slot):
        if isinstance(slot, GameSlot):
            return abs(slot.remaining_capacity() - slot.gameMin)  # Distance from gameMin
        return float('inf')  # Practices don't have a gameMin

    # Prioritize based on heuristics
    prioritized = sorted(
        valid_slots,
        key=lambda slot: (
            event.div != 9,  # False for div 9 (higher priority)
            int(slot.startTime.split(':')[0]) < 18,  # True if start time < 18
            distance_from_game_min(slot),  # Farther from gameMin is higher priority
            -slot.remaining_capacity()  # Use as a tiebreaker
        )
    )
    return prioritized

# Preprocess incompatible pairs
def preprocess_incompatible_pairs(not_compatible):
    incompatible_map = defaultdict(set)
    for pair in not_compatible:
        incompatible_map[pair[0]].add(pair[1])
        incompatible_map[pair[1]].add(pair[0])
    return incompatible_map


# And-Tree build
def build_tree(node, unscheduled_events, parent_slots, check_hard_constraints, eval_f, incompatible_map, depth=0):
    global best_schedule, best_eval_score, best_schedule_is_complete, iteration_count, unscheduled_events_count
    
    if depth > MAX_DEPTH:
        return
    
    iteration_count+=1
    if iteration_count > MAX_ITERATIONS:
        return

    # Evaluate the current schedule
    current_eval_score = eval_f(parent_slots, node.schedule)
    if not unscheduled_events:
        # If all events are scheduled
        if check_hard_constraints(node.schedule):
            node.sol = "yes"
            if not best_schedule_is_complete or current_eval_score < best_eval_score:
                best_eval_score = current_eval_score
                best_schedule = node.schedule.copy_schedule()
                best_schedule_is_complete = True
    else:
        # Save best partial schedule
        if not best_schedule_is_complete:
            if len(unscheduled_events) < unscheduled_events_count:
                unscheduled_events_count = len(unscheduled_events)
                best_eval_score = current_eval_score
                best_schedule = node.schedule.copy_schedule()
                node.schedule.print_schedule(current_eval_score)

    # Check for already-visited states
    state_hash = hash(frozenset(node.schedule.scheduleVersion.items()))
    if state_hash in checked_states:
        return
    checked_states.add(state_hash)

    # Reorder events for processing
    ordered_events = reorder_events(unscheduled_events, incompatible_map)

    # Process each event
    for event in ordered_events:
        prioritized_slots = prioritize_slots(event, parent_slots, incompatible_map)
        for slot in prioritized_slots:
            if isinstance(event, Game) and not isinstance(slot, GameSlot):
                continue
            if isinstance(event, Practice) and not isinstance(slot, PracticeSlot):
                continue

            # Create a copy of the current slots and schedule
            child_slots = [s.copy() for s in parent_slots]
            new_schedule = node.schedule.copy_schedule()
            copied_slot = slot.copy()

            # Assign the event to the slot
            new_schedule.assign_event(event, copied_slot)

            # Check the new schedule against hard constraints
            if not check_hard_constraints(new_schedule):
                # Unassign if invalid
                new_schedule.unassign_event(event, copied_slot)
                continue

            # Create a new child node
            child_node = Node(schedule=new_schedule, sol="?")
            node.add_child(child_node)

            # Continue recursion with remaining events
            remaining_events = [e for e in unscheduled_events if e != event]
            # print(f"DEBUG: Before recursion, schedule: {node.schedule.print_schedule(current_eval_score)}")
            build_tree(child_node, remaining_events, child_slots, check_hard_constraints, eval_f, incompatible_map, depth + 1)
            # print(f"DEBUG: After recursion, schedule: {node.schedule.print_schedule(current_eval_score)}")

            # Unassign event after exploring the branch
            new_schedule.unassign_event(event, copied_slot)


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

        build_tree(
            root, 
            unscheduled_events, 
            slots, 
            hardConstraints.check_hard_constraints, 
            softConstraints.eval, 
            incompatible_map
            )

    except Exception as e:
        print(f"An error occurred: {e}")
        print(traceback.format_exc())
        if best_schedule:
            print("\nBest schedule found before error: \n")
            best_schedule.print_schedule(best_eval_score)
        else:
            print("No valid schedule found before error.")
        return

    if best_schedule:
        print("\nBest schedule found: \n")
        best_schedule.print_schedule(best_eval_score)
    else:
        print("No valid schedule found.")
        
    output_file_path = os.path.join(os.getcwd(), "output_" + os.path.basename(parser.filename))
    with open(output_file_path, "w") as file:
        if best_schedule:
            print("\nBest schedule found: \n")
            best_schedule.print_schedule(best_eval_score)
            file.write(f"Eval-Value: {best_eval_score}\n")
            file.write(best_schedule.to_string())  # Ensure your schedule class has a `to_string` method
        else:
            print("No valid schedule found.")
            file.write("No valid schedule found.")

    return root 

if __name__ == "__main__":
    root_node = main()
