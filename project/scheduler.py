# CPSC 433 - Artificial Intelligence - Fall 2024
# Aditi Yadav
# Jaden Myers
# Minori Olguin
# Monica Nguyen
# Thi Ngoc Anh Nguyen

from game import Game
from practice import Practice
from practiceSlot import PracticeSlot
from gameSlot import GameSlot
from input_parser import InputParser

class Scheduler:
    def __init__(self, events=None):
        self.scheduleVersion = {}
        self.events = events if events is not None else []
        self.scheduled_events = []

    def add_slot(self, slot):
        if slot not in self.scheduleVersion:
            self.scheduleVersion[slot] = "$"

    def assign_event(self, event, slot):
        if isinstance(event, Game):
            slot.assignedGames.append(event)
        elif isinstance(event, Practice):
            slot.assignedPractices.append(event)
        self.scheduleVersion[slot] = event

    def remove_event(self, slot):
        if slot in self.scheduleVersion:
            self.scheduleVersion[slot] = "$"

    def get_schedule(self):
        return self.scheduleVersion

    # **ASSUMPTION**: the eval_value still gets calculated for a game slot or practice slot EVEN IF there are not enough games or practices that could be assigned to each game slot or practice slot to satisfy the gamemin or practicemin in the first place
    # **LIMITATIONS**: I believe will be incorrect if the input.txt file repeats the same game or practice slot twice or more (I don't think we would have to worry about this as all input files so far have unique game and practice slots provided)
    def calculate_eval_value(self, parent_slots, pen_gamemin, pen_practicemin):
        eval_value = 0

        sorted_schedule = sorted(
            [(event, slot) for slot, event in self.scheduleVersion.items() if event != "$"],
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
                    eval_value = eval_value + (parent_slot.gameMin - assigned_games) * pen_gamemin
            elif isinstance(parent_slot, PracticeSlot):
                if assigned_practices < parent_slot.pracMin:
                    eval_value = eval_value + (parent_slot.pracMin - assigned_practices) * pen_practicemin

        return eval_value

    def is_same_slot(self, slot1, slot2):
        return isinstance(slot1, type(slot2)) and slot1.day == slot2.day and slot1.startTime == slot2.startTime

    def print_schedule(self, parent_slots, pen_gamemin, pen_practicemin):
        eval_value = self.calculate_eval_value(parent_slots, pen_gamemin, pen_practicemin)
        print(f"\033[1mEval-value:\033[0m {eval_value}")

        id_width = 30
        slot_width = 20

        sorted_schedule = sorted(
            [(event, slot) for slot, event in self.scheduleVersion.items() if event != "$"],
            key=lambda x: x[0].id)

        for event, slot in sorted_schedule:
            slot_info = f": {slot.day}, {slot.startTime}"
            print(f"{event.id:<{id_width}}{slot_info:<{slot_width}}")

    def copy_schedule(self):
        new_schedule = Scheduler(events=self.events)
        new_schedule.scheduleVersion = self.scheduleVersion.copy()
        return new_schedule
