# CPSC 433 - Artificial Intelligence - Fall 2024
# Aditi Yadav
# Jaden Myers
# Minori Olguin
# Monica Nguyen
# Thi Ngoc Anh Nguyen

from input_parser import InputParser
from scheduler import Scheduler
from node import Node

def initialize_root(events, game_slots, practice_slots, partial_assign):
    
    root_schedule = Scheduler()
    
    filtered_game_slots = [
        slot for slot in game_slots
        if not (slot.day == "TU" and slot.startTime == "11:00")
    ]
    
    for slot in filtered_game_slots + practice_slots:
        root_schedule.add_slot(slot)
    
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

    root.schedule.print_schedule()

    return root

if __name__ == "__main__":
    root_node = main()
