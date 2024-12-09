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

    def unassign_event(self, event, slot):
        # Ensure the event and slot exist in the schedule
        if slot not in self.scheduleVersion:
            print(f"DEBUG: Slot {slot.id} not found in schedule.")
            return False

        # Check if the slot contains the event to be unassigned
        assigned_event = self.scheduleVersion.get(slot, "$")
        if assigned_event != event:
            print(f"DEBUG: Event {event.id} not assigned to slot {slot.id}.")
            return False

        # Unassign the event from the slot
        self.scheduleVersion[slot] = "$"  # Mark slot as unassigned

        # Update slot's internal state
        if isinstance(slot, GameSlot):
            slot.assignedGames.remove(event)
        elif isinstance(slot, PracticeSlot):
            slot.assignedPractices.remove(event)

        # Optionally, log the unassignment
        # print(f"DEBUG: Event {event.id} unassigned from slot {slot.id}.")
        return True

            

    def get_schedule(self):
        return self.scheduleVersion

    def print_schedule(self, eval_value):
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
