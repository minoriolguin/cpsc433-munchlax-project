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
    def eval(self, schedule):
        return (
            self.eval_min_filled(schedule) * self.input_parser.w_minfilled + 
            self.eval_pref(schedule) * self.input_parser.w_pref + 
            self.eval_pair(schedule) * self.input_parser.w_pair + 
            self.eval_sec_diff(schedule) * self.input_parser.w_secdiff
        )
        
    # Uses pen_gamemin and pen_practice min to compute penalty
    def eval_min_filled(self, schedule):
        penalty = 0
        
        # Iterate through the scheduled slots
        for slot in schedule.scheduleVersion:
            if isinstance(slot, GameSlot):
                unfilled_games = slot.gameMin - len(slot.assignedGames)
                if unfilled_games > 0: 
                    penalty += unfilled_games * self.input_parser.pen_gamemin
            if isinstance(slot, PracticeSlot):
                unfilled_practices = slot.pracMin - len(slot.assignedPractices)
                if unfilled_practices > 0:
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

        # Iterate through the list of pairs
        for pair in self.input_parser.pair:
            event1_id, event2_id = pair
            event1_slot = None
            event2_slot = None

            # Find the slots assigned to each event in the pair
            for slot, event in schedule.scheduleVersion.items():
                if event != "$":
                    if event.id == event1_id:
                        event1_slot = slot
                    elif event.id == event2_id:
                        event2_slot = slot

            # If both events are scheduled but in different slots, apply a penalty
            if event1_slot and event2_slot and event1_slot != event2_slot:
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
                    print(f"DEBUG: Overlapping divisions in slot {day}, {start_time}, tier {tier}: {count} divisions, penalty: {penalty}")

        return penalty


