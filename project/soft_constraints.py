# CPSC 433 - Artificial Intelligence - Fall 2024
# Aditi Yadav
# Jaden Myers
# Minori Olguin
# Monica Nguyen
# Thi Ngoc Anh Nguyen

from collections import defaultdict
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
            # If game slot
            if isinstance(slot, GameSlot):
                unfilled_games = slot.gameMin - len(slot.assignedGames) # check if theres under filled games (less than gameMin)
                if unfilled_games > 0: 
                    penalty+= unfilled_games * self.input_parser.pen_gamemin # add penalty                
            if isinstance(slot, PracticeSlot):
                unfilled_practices = slot.pracMin - len(slot.assignedPractices) # check if theres under filled practices (less than gameMax)
                if unfilled_practices > 0:
                    penalty+= unfilled_practices * self.input_parser.pen_practicemin # add penalty
        return penalty

    # Uses the individual references in input file under "Preferences"
    def eval_pref(self, schedule):
        penalty = 0

        preferences_map = {
            pref['id']: pref for pref in self.input_parser.preferences
        }

        # Iterate through the schedule to evaluate preferences
        for slot, event in schedule.scheduleVersion.items(): 
            if event != "$":
                preferred_time = preferences_map.get(event.id)
                if preferred_time:  # if there's a preference for this event
                    if slot.day != preferred_time['day'] or str(slot.startTime) != str(preferred_time['time']):
                        # add penalty for mismatched day or time
                        penalty += int(preferred_time['score'])

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
        tier_map = defaultdict(list)  # Use defaultdict to avoid initialization issues

        # Group divisions by slot (identified by name, day, and start time)
        for slot, event in schedule.scheduleVersion.items():
            if event != "$" and isinstance(event, Game):
                tier_map[(slot.id, slot.day, slot.startTime)].append(event.div)

        # Check for overlapping divisions in the same slot
        for (id, day, start_time), divisions in tier_map.items():
            if len(divisions) > 1:  # More than one division in the same slot
                # Add penalty for each overlapping division
                penalty += (len(divisions) - 1) * self.input_parser.pen_section

        return penalty

