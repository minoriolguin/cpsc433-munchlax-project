# CPSC 433 - Artificial Intelligence - Fall 2024
# Aditi Yadav
# Jaden Myers
# Minori Olguin
# Monica Nguyen
# Thi Ngoc Anh Nguyen

from input_parser import InputParser
from practiceSlot import PracticeSlot
from gameSlot import GameSlot

class HardConstraints:
    def __init__(self, input_parser: InputParser):
          self.input_parser = input_parser

    # function to check if all hard constraints are satisfied
    def check_hard_constraints(self, schedule):
        # hard constraint 1
        if self.over_gamemax():
            return False
        
        # hard constraint 2
        if self.over_practicemax():
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
        if self.check_overlapping():
            return False
        
        # city of calgary hard constraint 4
        if self.check_meeting_time():
            return False
        
        # city of calgary hard constraint 5
        if self.check_special_practices():
            return False
        
        if self.evening_divisions():
            return False

        # at this point all the hard constraints have passed
        return True
        
    def over_gamemax(self):
        for game_slot in self.input_parser.gameSlots:
            if len(game_slot.assignedGames) > game_slot.gameMax:
                return True
        
        # at this point no game slot is over games max so this hard constraint passes
        return False

    def over_practicemax(self):
        for practice_slot in self.input_parser.practiceSlots:
            if len(practice_slot.assignedPractices) > practice_slot.pracMax:
                return True
        
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

    def not_corresponding_games(self): # this function isn't needed? combine mon, wed, fri slots in input parser?
        return False

    def not_corresponding_practices(self):
        return False

    def evening_divisions(self):
        for gameSlot in self.input_parser.gameSlots:
            for game in gameSlot.assignedGames:
                if str(game.div)[0] == "9" and int(str(gameSlot.startTime)[0:2]) < 12:
                    return True
        
        return False

    def check_overlapping(self):
        return False

    def check_meeting_time(self):
        return False

    def check_special_practices(self):
        return False
