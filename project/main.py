# CPSC 433 - Artificial Intelligence - Fall 2024
# Aditi Yadav
# Jaden Myers
# Minori Olguin
# Monica Nguyen
# Thi Ngoc Anh Nguyen

from game import Game
from practice import Practice
from gameSlot import GameSlot
from practiceSlot import PracticeSlot
from input_parser import InputParser
from scheduler import Scheduler
from node import Node
from collections import defaultdict
from hardConstraints import HardConstraints

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
                print(f"Failed to find valid slot for special practice {special_practice_id}.")
                return None

            special_practice = next(
                (e for e in events if e.id == special_practice_id), None)
            if not special_practice:
                print(f"Special practice {special_practice_id} not found in events.")
                return None

            root_schedule.assign_event(special_practice, special_practice_slot)
            practice_slots.remove(special_practice_slot)

    # assigns any partial assignments for the schedule
    for assign in partial_assign:
        if 'id' not in assign or 'day' not in assign or 'time' not in assign:
            print(f"Invalid partial assignment format: {assign}")
            return None 

        event_id = assign['id']
        day = assign['day'].strip()
        time = assign['time'].strip()

        event = next((e for e in events if e.id == event_id), None)
        if not event:
            print(f"Event with ID '{event_id}' not found in events.")
            return None 

        slot = next((s for s in filtered_game_slots + practice_slots 
                     if s.day == day and s.startTime == time), None)
        if not slot:
            print(f"Slot with day '{day}' and time '{time}' not found.")
            return None 

        root_schedule.assign_event(event, slot)
                
    return Node(schedule=root_schedule, sol="?")

# Helper function to sort by team (so if a team is selected it will try the team's game then their practice)
def group_events_by_team(events):
    grouped = defaultdict(list)
    for event in events:
        team_id = f"{event.league}{event.tier}{event.div}"
        grouped[team_id].append(event)
    return grouped

# And-Tree build
def build_tree(node, unscheduled_events, parent_slots, check_hard_constraints, depth=0):
    # Base case: check if all events have been scheduled
    if not unscheduled_events:
        if check_hard_constraints(node.schedule): 
            print("\n********Valid Schedule Found********")
            node.schedule.print_schedule()
            print("\n")
            node.sol = "yes"
        else:
            print("\nInvalid Schedule:")
            node.schedule.print_schedule()
            node.sol = "?"
            print("\n")
        return

    # Group events by team and prioritize
    events_by_team = group_events_by_team(unscheduled_events)

    for team_id, team_events in events_by_team.items():
        for event in team_events:
            for slot in parent_slots:
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
                    print(f"Skipping invalid schedule: {event.id} in {slot.day}, {slot.startTime}")
                    continue

                # Create a new node if valid
                child_node = Node(schedule=new_schedule, sol="?")
                node.add_child(child_node)

                # Continue to use recursion for remaining events
                remaining_events = [e for e in unscheduled_events if e != event]
                build_tree(child_node, remaining_events, child_slots, check_hard_constraints, depth + 1)


# Main method 
def main():
    parser = InputParser()
    parser.main()

    events = parser.games + parser.practices
    game_slots = parser.gameSlots
    practice_slots = parser.practiceSlots
    partial_assign = parser.partial_assign

    try:
        root = initialize_root(events, game_slots, practice_slots, partial_assign)
    except ValueError as e:
        print(f"Error initializing root: {e}")
        return None
    
    unscheduled_events = [event for event in events if not any(assign['id'] == event.id for assign in partial_assign)]
    slots = game_slots + practice_slots

    hardConstraints = HardConstraints(parser)

    build_tree(root, unscheduled_events, slots, hardConstraints.check_hard_constraints)

    return root

if __name__ == "__main__":
    root_node = main()