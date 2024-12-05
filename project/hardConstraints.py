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
        if self.notcompatible(schedule):
            return False

        # hard constraint 5
        # if self.partassign():
        #     return False

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
        num_games = {}
        for slot, game in schedule.scheduleVersion.items():
            if game != "$" and isinstance(slot, GameSlot):
                if slot.id not in num_games.keys():
                    num_games[slot.id] = 1
                else:
                    if num_games[slot.id] + 1 > slot.gameMax:
                        return True
                    else:
                        num_games[slot.id] += 1
        # at this point no game slot is over games max so this hard constraint passes
        return False

    def over_practicemax(self, schedule):
        num_practices = {}
        for slot, practice in schedule.scheduleVersion.items():
            if practice != "$" and isinstance(slot, PracticeSlot):
                if slot.id not in num_practices.keys():
                    num_practices[slot.id] = 1
                else:
                    if num_practices[slot.id] + 1 > slot.pracMax:
                        return True
                    else:
                        num_practices[slot.id] += 1
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

    def notcompatible(self, schedule):
        for incompatable_pair in self.input_parser.not_compatible:

            # find slot for event 1
            event1_slot = None
            event2_slot = None
            for slot, event in schedule.scheduleVersion.items():
                if event != "$":
                    if event.id == incompatable_pair[0]:
                        event1_slot = slot
                    elif event.id == incompatable_pair[1]:
                        event2_slot = slot
            
            if event1_slot is not None and event2_slot is not None:
                d1 = event1_slot.day
                d2 = event2_slot.day
                if d1 == d2 or (d1 == "FR" and d2 == "MO") or (d1 == "MO" and d2 == "FR"):
                    
                    # convert the the times to ints
                    if len(str(event1_slot.startTime)) == 4:
                        start1 = int(str(event1_slot.startTime)[0:1])
                    else:
                        start1 = int(str(event1_slot.startTime)[0:2])

                    if int(str(event1_slot.startTime)[len(str(event1_slot.startTime))-2:len(str(event1_slot.startTime))]) == 30:
                        start1 += 0.5
                    
                    # convert the the times to ints
                    if len(str(event2_slot.startTime)) == 4:
                        start2 = int(str(event2_slot.startTime)[0:1])
                    else:
                        start2 = int(str(event2_slot.startTime)[0:2])

                    if int(str(event2_slot.startTime)[len(str(event2_slot.startTime))-2:len(str(event2_slot.startTime))]) == 30:
                        start2 += 0.5

                    # calculate time interval
                    end1 = 0
                    end2 = 0

                    if d1 == "MO":
                        end1 = start1 + 1
                    elif d1 == "TU":
                        if is_game(incompatable_pair[0]):
                            end1 = start1 + 1.5
                        else:
                            end1 = start1 + 2
                    else:
                        end1 = start1 + 2
                    
                    if d1 == "MO":
                        end2 = start2 + 1
                    elif d1 == "TU":
                        if is_game(incompatable_pair[1]):
                            end2 = start2 + 1.5
                        else:
                            end2 = start2 + 2
                    else:
                        end2 = start2 + 2
                    
                    # check for overlap in the time intervals
                    if max(start1, start2) < min(end1, end2):
                        print("here")
                        return True

        # # at this point no non-compatible pairs share the same slot
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

def is_game(id):
    if "PRC" in id.split():
        return False
    else:
        return True