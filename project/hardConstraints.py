# CPSC 433 - Artificial Intelligence - Fall 2024
# Aditi Yadav
# Jaden Myers
# Minori Olguin
# Monica Nguyen
# Thi Ngoc Anh Nguyen

from input_parser import InputParser
from practiceSlot import PracticeSlot
from gameSlot import GameSlot
from practice import Practice

class HardConstraints:
    def __init__(self, input_parser: InputParser):
          self.input_parser = input_parser

    # function to check if all hard constraints are satisfied
    def check_hard_constraints(self, schedule):
        # hard constraint 1
        if self.over_gamemax(schedule):
            return False
        
        # hard constraint 2
        if self.over_practicemax(schedule):
            return False
        
        # hard constraint 3
        if self.assign_equal():
            return False
        
        # hard constraint 4
        if self.notcompatible():
            return False
        
        # hard constraint 5
        if self.partassign():
            return False
        
        # hard constraint 6
        if self.unwanted():
            return False
        
        # city of calgary constraints:

        # city of calgary hard constraint 1
        if self.not_corresponding_games(): # check for both (monday, wednesday, friday) and (tuedsay, thursday)
            return False
        
        # city of calgary hard constraint 2
        if self.not_corresponding_practices(): # check for both (monday, wednesday) and (tuedsay, thursday)
            return False
        
        # city of calgary hard constraint 3
        if self.check_overlapping(schedule):
            return False
        
        # city of calgary hard constraint 4
        if self.check_meeting_time():
            return False
        
        # city of calgary hard constraint 5
        if self.check_special_practices():
            return False
        
        if self.evening_divisions(schedule):
            return False

        # at this point all the hard constraints have passed
        return True
    
    def over_gamemax(self, schedule): # can probably be combined with over_practicemax
        for slot in schedule.scheduleVersion.keys():
            if isinstance(slot, GameSlot):
                if len(slot.assignedGames) > slot.gameMax:
                    return True
        # at this point no game slot is over games max so this hard constraint passes
        return False

    def over_practicemax(self, schedule):
        for slot in schedule.scheduleVersion.keys():
            if isinstance(slot, PracticeSlot):
                if len(slot.assignedPractices) > slot.pracMax:
                    return True
            pass
        # at this point no practice slot is over practice max so this hard constraint passes
        return False

    def assign_equal(self):
        # for slot in self.input_parser.slots:
        #     games = slot.assignGames
        #     practices = slot.assignPractices

        #     # check for overlap in divisions
        #     game_divisions = set(game.div for game in games)
        #     practice_divisions = set(practice.div for practice in practices)

        #     # check if theres any common division
        #     if game_divisions.intersection(practice_divisions):
        #         return True  # constraint violated because an overlap between practices and games is found
        return False 

    def notcompatible(self):
        # combine all the slots into a single list
        # all_slots = self.input_parser.gameSlots + self.input_parser.practiceSlots

        # # check each non compatible pair
        # for event_a, event_b in self.input_parser.not_compatible:
        #     # check if both the events are assigned to the same slot
        #     if any( (event_a in slot.assignedGames + slot.assignedPractices) and (event_b in slot.assignGames + slot.assignPractices)
        #         for slot in all_slots):
        #         return True  # constraint violated

        # # at this point no not-compatible pairs share the same slot
        return False

    def partassign(self):
        
        for partial_assg in self.input_parser.partial_assign:
            event, assigned_slot = partial_assg[0], partial_assg[1]

            # check to skip if assigned slot is the placeholder - "$"
            if assigned_slot == "$":
                continue
            
            for slot in self.input_parser.gameSlots + self.input_parser.practiceSlots:
                if slot == assigned_slot:
                    if event not in slot.assignGames and event not in slot.assignPractices:
                        return True
        return False


    def unwanted(self):
        # go through all the unwanted constraints
        for unwanted_constraints in self.input_parser.unwanted:
            event, unwanted_slot = unwanted_constraints['id'], unwanted_constraints['time']

        # check if event is assigned to unwanted slot
        for slot in self.input_parser.gameSlots + self.input_parser.practiceSlots:
            if slot == unwanted_slot:
                if event in slot.assignGames or event in slot.assignPractices:
                    return True # constraint violated
        return False

    def not_corresponding_games(self): # is this function needed? combine mon, wed, fri slots in input parser?
        return False

    def not_corresponding_practices(self): # is this function needed? combine mon, wed, fri slots in input parser?
        return False

    def evening_divisions(self, schedule):
        for slot in schedule.scheduleVersion.keys():
            if isinstance(slot, PracticeSlot):
                for practice in slot.assignedPractices:
                    if practice.div:
                        if str(practice.div)[0] == "9":
                            if len(str(slot.startTime)) == 4:
                                start = int(str(slot.startTime)[0:1])
                            else:
                                start = int(str(slot.startTime)[0:2])
                            if start < 18:
                                return True
            elif isinstance(slot, GameSlot):
                for game in slot.assignedGames:
                    if game.div:
                        if str(game.div)[0] == "9":
                            if len(str(slot.startTime)) == 4:
                                start = int(str(slot.startTime)[0:1])
                            else:
                                start = int(str(slot.startTime)[0:2])
                            if start < 18:
                                return True
       
        return False

    def check_overlapping(self, schedule):
        levels = ["U15", "U16", "U17", "U19"]
        tier_times = {}
        for slot in schedule.scheduleVersion.keys():
            if isinstance(slot, GameSlot):
                for game in slot.assignedGames:
                    u_level = game.tier[0:3]
                    if u_level in levels:
                        if game.tier in tier_times.keys():
                            if (slot.day, slot.startTime) in tier_times[game.tier]:
                                # overlap found, hard constraint failed
                                return True
                            else:
                                # keep track of times with U15/U16/U17/U19 games assigned to them
                                tier_times[game.tier].append((slot.day, slot.startTime))
                        else:
                            # keep track of tiers
                            tier_times[game.tier] = [(slot.day, slot.startTime)]
                            
        return False

    def check_meeting_time(self): # implemented in main
        return False

    def check_special_practices(self): # implemented in main
        return False
