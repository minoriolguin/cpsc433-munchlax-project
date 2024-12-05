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
    def calculate_eval_value(self, pen_gamemin, pen_practicemin):
        eval_value = 0

        for slot, event in self.scheduleVersion.items():
            if isinstance(slot, GameSlot):
                eval_value += (slot.gameMin - len(slot.assignedGames)) * pen_gamemin
            elif isinstance(slot, PracticeSlot):
                eval_value += slot.pracMin - len(slot.assignedPractices) * pen_practicemin

        return eval_value

    def print_schedule(self, pen_gamemin, pen_practicemin):
        eval_value = self.calculate_eval_value(pen_gamemin, pen_practicemin)
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
