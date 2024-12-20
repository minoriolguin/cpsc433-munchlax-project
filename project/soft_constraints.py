# CPSC 433 - Artificial Intelligence - Fall 2024
# Aditi Yadav
# Jaden Myers
# Minori Olguin
# Monica Nguyen
# Thi Ngoc Anh Nguyen

from collections import defaultdict
from itertools import combinations
from input_parser import InputParser
from practice import Practice
from game import Game
from gameSlot import GameSlot
from practiceSlot import PracticeSlot

class SoftConstraints:
    def __init__(self, input_parser : InputParser):        
        self.input_parser = input_parser

    # calculates the total eval value
    def eval(self, current_slots, schedule):
        return (
            self.eval_min_filled(current_slots, schedule) * self.input_parser.w_minfilled + 
            self.eval_pref(schedule) * self.input_parser.w_pref + 
            self.eval_pair(schedule) * self.input_parser.w_pair + 
            self.eval_sec_diff(schedule) * self.input_parser.w_secdiff
        )
        
    def is_same_slot(self, slot1, slot2):
        if not hasattr(slot1, 'day') or not hasattr(slot2, 'day'):
            # print(f"Invalid slot comparison: slot1={slot1}, slot2={slot2}")
            return False
        return (
            slot1.day == slot2.day and
            slot1.startTime == slot2.startTime
        )

            
    # Uses pen_gamemin and pen_practicemin to compute penalty
    def eval_min_filled(self, current_slots, schedule):
        penalty = 0
        processed_slots = set()  # Track slots that have already been processed

        for slot in current_slots:
            # Generate a unique identifier for the slot to prevent duplicates
            slot_key = (slot.day, slot.startTime, type(slot).__name__)

            # Skip the slot if it's already been processed
            if slot_key in processed_slots:
                continue

            # Mark the slot as processed
            processed_slots.add(slot_key)

            # Collect assigned events for the slot
            assigned_games = []
            assigned_practices = []

            for assigned_slot, event in schedule.scheduleVersion.items():
                if event == "$":  # Skip placeholders
                    continue

                # Check if the assigned slot matches the current slot
                if self.is_same_slot(slot, assigned_slot):
                    if isinstance(event, Game):
                        assigned_games.append(event)
                    elif isinstance(event, Practice):
                        assigned_practices.append(event)

            # Update slot's assigned events
            if isinstance(slot, GameSlot):
                slot.assignedGames = assigned_games

                # Penalize only if the slot has been partially or fully scheduled
                if assigned_games or slot.gameMin > 0:
                    unfilled_games = max(0, slot.gameMin - len(slot.assignedGames))
                    penalty += unfilled_games * self.input_parser.pen_gamemin

            elif isinstance(slot, PracticeSlot):
                slot.assignedPractices = assigned_practices

                # Penalize only if the slot has been partially or fully scheduled
                if assigned_practices or slot.pracMin > 0:
                    unfilled_practices = max(0, slot.pracMin - len(slot.assignedPractices))
                    penalty += unfilled_practices * self.input_parser.pen_practicemin

        return penalty

    # Uses the individual references in input file under "Preferences"
    def eval_pref(self, schedule):
        penalty = 0

        for pref in self.input_parser.preferences:
            for slot, event in schedule.scheduleVersion.items():
                if (event != "$" and event.id == pref['id']):
                    if slot.day != pref['day'] or str(slot.startTime) != str(pref['time']):
                    #print(f"Mismatch detected: Event {event.id} assigned to {slot.day} {slot.startTime}, preferred {pref['day']} {pref['time']}")
                        penalty += int(pref['score'])
                        # print(event)
        # print(f'penalty {penalty} w_penalty {self.input_parser.w_pref} res {penalty*self.input_parser.w_pref}')
        return penalty

    # Uses pen_notpaired to calculate penalty
    def eval_pair(self, schedule):
        penalty = 0 

        # Preprocess the schedule
        event_to_slot = {
            event.id: slot for slot, event in schedule.scheduleVersion.items() if event != "$"
        }

        # Iterate through the list of pairs
        for event1_id, event2_id in self.input_parser.pair:
            event1_slot = event_to_slot.get(event1_id)
            event2_slot = event_to_slot.get(event2_id)

            # Check if events are not in the same slot or are not scheduled
            if (
                not event1_slot
                or not event2_slot
                or (event1_slot.day != event2_slot.day or event1_slot.startTime != event2_slot.startTime)
            ):
                penalty += self.input_parser.pen_notpaired

        return penalty
    
    # Uses pen_section to calculate penalty
    def eval_sec_diff(self, schedule):
        penalty = 0
        tier_map = defaultdict(list)  # Group by slot

        # Group divisions by slot (consider tier + division)
        for slot, event in schedule.scheduleVersion.items():
            if event != "$" and isinstance(event, Game):
                tier_div = (event.tier, event.div)
                tier_map[(slot.id, slot.day, slot.startTime)].append(tier_div)

        # Penalize overlapping divisions within the same tier
        for (slot_id, day, start_time), tier_divisions in tier_map.items():
            overlapping_tiers = defaultdict(int)
            for tier, div in tier_divisions:
                overlapping_tiers[tier] += 1  # Count divisions per tier

            for tier, count in overlapping_tiers.items():
                if count > 1:  # More than one division from the same tier
                    penalty += (count - 1) * self.input_parser.pen_section
                    # print(f"DEBUG: Overlapping divisions in slot {day}, {start_time}, tier {tier}: {count} divisions, penalty: {penalty}")

        return penalty


