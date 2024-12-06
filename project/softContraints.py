from input_parser import InputParser
from practice import Practice
from game import Game
from gameSlot import GameSlot
from practiceSlot import PracticeSlot

class SoftConstraints:
    def __init__(self, input_parser: InputParser):
        self.input_parser = input_parser

    def check_minimum_slot_usage(self, schedule):
        penalty = 0

        print("Debug: Starting Minimum Slot Usage Check")
        for slot, event in schedule.scheduleVersion.items():
            if isinstance(slot, GameSlot):
                assigned_games = len([e for e in slot.assignedGames if e != "$"])
                print(f"Game Slot: {slot.id}, Assigned Games: {assigned_games}, Min Required: {slot.gameMin}")
                if assigned_games < slot.gameMin:
                    slot_penalty = (slot.gameMin - assigned_games) * self.input_parser.pengamemin
                    print(f"Penalty for Slot {slot.id}: {slot_penalty}")
                    penalty += slot_penalty
            elif isinstance(slot, PracticeSlot):
                assigned_practices = len([e for e in slot.assignedPractices if e != "$"])
                print(f"Practice Slot: {slot.id}, Assigned Practices: {assigned_practices}, Min Required: {slot.pracMin}")
                if assigned_practices < slot.pracMin:
                    slot_penalty = (slot.pracMin - assigned_practices) * self.input_parser.penpracticemin
                    print(f"Penalty for Slot {slot.id}: {slot_penalty}")
                    penalty += slot_penalty

        print(f"Total Minimum Slot Usage Penalty: {penalty}")
        return penalty

    def check_preferred_time_slots(self, schedule):
        penalty = 0

        print("Debug: Starting Preferred Time Slots Check")
        for slot, event in schedule.scheduleVersion.items():
            if event != "$":
                preferred_time = next(
                    (pref for pref in self.input_parser.preferences if pref['id'] == event.id),
                    None
                )
                if slot.day != preferred_time['day'] or str(slot.startTime) != str(preferred_time['time']):
                    print(f"Mismatch detected: Event {event.id} assigned to {slot.day} {slot.startTime}, preferred {preferred_time['day']} {preferred_time['time']}")
                    penalty += int(preferred_time['score'])



        print(f"Total Preferred Time Slots Penalty: {penalty}")
        return penalty
    
    def check_paired_events(self, schedule):
        penalty = 0

        print("Debug: Starting Paired Events Check")

        for pair in self.input_parser.pair:
            event1_id, event2_id = pair
            event1_slot = None
            event2_slot = None

            for slot, event in schedule.scheduleVersion.items():
                if event != "$":
                    if event.id == event1_id:
                        event1_slot = slot
                    elif event.id == event2_id:
                        event2_slot = slot

            if event1_slot and event2_slot and event1_slot != event2_slot:
                print(f"Unpaired events: {event1_id} in {event1_slot} and {event2_id} in {event2_slot}")
                penalty += self.parser.pen_notpaired


            
        print(f"Total Paired Events Penalty: {penalty}")
        return penalty
