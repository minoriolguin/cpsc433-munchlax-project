from input_parser import InputParser
from practice import Practice
from game import Game
from gameSlot import GameSlot
from practiceSlot import PracticeSlot

class SoftConstraints:
    def __init__(self, input_parser: InputParser):
        self.input_parser = input_parser

    # **ASSUMPTION**: the eval_value still gets calculated for a game slot or practice slot EVEN IF there are not enough games or practices that could be assigned to each game slot or practice slot to satisfy the gamemin or practicemin in the first place
    # **LIMITATIONS**: I believe will be incorrect if the input.txt file repeats the same game or practice slot twice or more (I don't think we would have to worry about this as all input files so far have unique game and practice slots provided)
    def check_minimum_slot_usage(self, schedule, parent_slots):
        penalty = 0

        sorted_schedule = sorted(
            [(event, slot) for slot, event in schedule.scheduleVersion.items() if event != "$"],
            key=lambda x: x[0].id)

        for parent_slot in parent_slots:
            assigned_games = 0
            assigned_practices = 0

            for event, slot in sorted_schedule:
                if self.is_same_slot(slot, parent_slot):
                    if isinstance(slot, GameSlot):
                        assigned_games = assigned_games + 1
                    elif isinstance(slot, PracticeSlot):
                        assigned_practices = assigned_practices + 1

            if isinstance(parent_slot, GameSlot):
                if assigned_games < parent_slot.gameMin:
                    penalty = penalty + (parent_slot.gameMin - assigned_games) * self.input_parser.pengamemin
            elif isinstance(parent_slot, PracticeSlot):
                if assigned_practices < parent_slot.pracMin:
                    penalty = penalty + (parent_slot.pracMin - assigned_practices) * self.input_parser.penpracticemin

        return penalty

    def is_same_slot(self, slot1, slot2):
        return isinstance(slot1, type(slot2)) and slot1.day == slot2.day and slot1.startTime == slot2.startTime

    def check_preferred_time_slots(self, schedule):
        #print("Debug: Starting Preferred Time Slots Check")
        penalty = 0

        for pref in self.input_parser.preferences:
            for slot, event in schedule.scheduleVersion.items():
                if (event != "$" and event.id == pref['id']):
                    if slot.day != pref['day'] or str(slot.startTime) != str(pref['time']):
                    #print(f"Mismatch detected: Event {event.id} assigned to {slot.day} {slot.startTime}, preferred {pref['day']} {pref['time']}")
                        penalty += int(pref['score'])
                        print(event)

        return penalty*self.input_parser.wpref

    def check_paired_events(self, schedule):
        penalty = 0
        #print("Debug: Starting Paired Events Check")

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

            if event1_slot and event2_slot and (event1_slot.day != event2_slot.day or event1_slot.startTime != event2_slot.startTime):
                # print(f"Unpaired events: {event1_id} in {event1_slot} and {event2_id} in {event2_slot}")
                penalty += self.input_parser.pennotpaired

        #print(f"Total Paired Events Penalty: {penalty}")
        return penalty*self.input_parser.wpair


    def check_avoid_overloading_divisions(self, schedule):
        
        penalty = 0
        print("Debug: Starting Overloading Divisions Check")

        # Dictionary to track slots and their assigned divisions
        slot_divisions = {}

        # Iterate through all assigned slots
        for slot, event in schedule.scheduleVersion.items():
            if event != "$":  # Skip unassigned events
                slot_key = f"{slot.day} {slot.startTime}"  # Unique key for each slot
                if slot_key not in slot_divisions:
                    slot_divisions[slot_key] = []
                slot_divisions[slot_key].append(event.div)  # Access division using 'div'

        # Check for overloading divisions in the same slot
        for slot_key, divisions in slot_divisions.items():
            unique_divisions = set(divisions)
            overload_count = len(divisions) - len(unique_divisions)
            if overload_count > 0:  # If there are overlaps
                slot_penalty = overload_count * self.input_parser.penalty_overload
                print(f"Slot: {slot_key}, Overloaded Divisions: {overload_count}, Penalty: {slot_penalty}")
                penalty += slot_penalty

        print(f"Total Overloading Divisions Penalty: {penalty}")
        return penalty
    
    def check_avoid_overloading_divisions(self, schedule):
            total_penalty = 0
            for slot, events in schedule.scheduleVersion.items():
                if not isinstance(events, list):
                    events = [events]
                grouped_divisions = {}
                for event in events:
                    if isinstance(event, Game) or isinstance(event, Practice):
                        key = (event.league, event.tier)
                        if key not in grouped_divisions:
                            grouped_divisions[key] = 0
                        grouped_divisions[key] += 1
                for count in grouped_divisions.values():
                    if count > 1:
                        total_penalty += (count - 1) * self.input_parser.pen_section
            return total_penalty
    
    def check_spread_of_events(self, schedule):
        total_penalty = 0
        slot_usage = {}
        for slot, events in schedule.scheduleVersion.items():
            if isinstance(events, (Game, Practice)):
                events = [events]
            slot_usage[slot] = len(events)
        max_events = max(slot_usage.values()) if slot_usage else 0
        min_events = min(slot_usage.values()) if slot_usage else 0
        if max_events - min_events > 1:
            total_penalty += (max_events - min_events) * self.input_parser.w_minfilled
        return total_penalty