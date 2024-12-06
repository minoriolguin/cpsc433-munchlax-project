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
        penalty = 0

        #print("Debug: Starting Preferred Time Slots Check")
        for slot, event in schedule.scheduleVersion.items():
            if event != "$":
                preferred_time = next(
                    (pref for pref in self.input_parser.preferences if pref['id'] == event.id),
                    None
                )

                if preferred_time is not None:
                    if slot.day != preferred_time['day'] or str(slot.startTime) != str(preferred_time['time']):
                        #print(f"Mismatch detected: Event {event.id} assigned to {slot.day} {slot.startTime}, preferred {preferred_time['day']} {preferred_time['time']}")
                        penalty += int(preferred_time['score'])

        return penalty

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

            if event1_slot and event2_slot and event1_slot != event2_slot:
                #print(f"Unpaired events: {event1_id} in {event1_slot} and {event2_id} in {event2_slot}")
                penalty += self.input_parser.pen_notpaired



        #print(f"Total Paired Events Penalty: {penalty}")
        return penalty
