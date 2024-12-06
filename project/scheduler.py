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

    def calculate_eval_value(self, parent_slots, softConstraints):
        minimum_slot_usage_penalty = softConstraints.check_minimum_slot_usage(self, parent_slots)
        print(f"Minimum Slot Usage Penalty: {minimum_slot_usage_penalty}")

        preferred_slot_usage_penalty = softConstraints.check_preferred_time_slots(self)
        print(f"Preferred Slot Usage Penalty: {preferred_slot_usage_penalty}")

        paired_events_penalty = softConstraints.check_paired_events(self)
        print(f"Paired Events Penalty: {paired_events_penalty}")

        overloading_penalty = softConstraints.check_avoid_overloading_divisions(self)
        print(f"Overloading Penalty: {overloading_penalty}")

        spread_of_events_penalty = softConstraints.check_spread_of_events(self)
        print(f"Spread of Events Penalty: {spread_of_events_penalty}")


        eval_value = minimum_slot_usage_penalty + preferred_slot_usage_penalty + paired_events_penalty + overloading_penalty + spread_of_events_penalty

        return eval_value

    def print_schedule(self, parent_slots, softConstraints):
        eval_value = self.calculate_eval_value(parent_slots, softConstraints)
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
