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
        # Update the internal state of the slot
        if isinstance(slot, GameSlot):
            # print(f"DEBUG: Unassigning event {event.id} from slot {slot.id}.")
            slot.assignedGames.remove(event)
        elif isinstance(slot, PracticeSlot):
            # print(f"DEBUG: Unassigning event {event.id} from slot {slot.id}.")
            slot.assignedPractices.remove(event)
            

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

    def to_string(self):
        output = []

        id_width = 30
        slot_width = 20

        # Sort schedule by event ID
        sorted_schedule = sorted(
            [(event, slot) for slot, event in self.scheduleVersion.items() if event != "$"],
            key=lambda x: x[0].id
        )

        for event, slot in sorted_schedule:
            slot_info = f": {slot.day}, {slot.startTime}"
            output.append(f"{event.id:<{id_width}}{slot_info:<{slot_width}}")
        
        return "\n".join(output)

