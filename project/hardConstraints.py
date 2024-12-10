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

        # add assocciated games and practices to the incompatability list
        # so that we can reuse the compatability check to tell if assocciated practices and games are overlapping
        # (hard assignment 3 in the project description)
        for practice in input_parser.practices:
            for game in input_parser.games:
                if practice.div == "":
                    if game.league == practice.league and game.tier == practice.tier:
                        input_parser.not_compatible.append([game.id, practice.id])
                else:
                    if game.league == practice.league and game.tier == practice.tier and game.div == practice.div:
                        input_parser.not_compatible.append([game.id, practice.id])
        
        levels = ["U15", "U16", "U17", "U19"]
        for game in input_parser.games:
            u_level = game.tier[0:3]
            if u_level in levels:
                for game_incompatable in input_parser.games:
                    u_level2 = game_incompatable.tier[0:3]
                    if u_level2 in levels:
                        input_parser.not_compatible.append([game.id, game_incompatable.id])

    # function to check if all hard constraints are satisfied
    def check_hard_constraints(self, schedule):
        if self.over_gamemax(schedule):
            print(f"DEBUG: Failed over_gamemax")
            return False
        if self.over_practicemax(schedule):
            print(f"DEBUG: Failed over_practicemax")
            return False
        if self.notcompatible(schedule):
            # print(f"DEBUG: Failed notcompatible")
            return False
        if self.unwanted(schedule):
            print(f"DEBUG: Failed unwanted")
            return False
        # if self.check_overlapping(schedule):
        #     print(f"DEBUG: Failed overlapping")
        #     return False
        if self.evening_divisions(schedule):
            print(f"DEBUG: Failed evening_divisions")
            return False
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

    def notcompatible(self, schedule):
        for incompatible_pair in self.input_parser.not_compatible:

            # find slot for event 1
            event1_slot = None
            event2_slot = None
            for slot, event in schedule.scheduleVersion.items():
                if event != "$":
                    if event.id == incompatible_pair[0]:
                        event1_slot = slot
                    elif event.id == incompatible_pair[1]:
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
                        if is_game(incompatible_pair[0]):
                            end1 = start1 + 1.5
                        else:
                            end1 = start1 + 2
                    else:
                        end1 = start1 + 2

                    if d2 == "MO":
                        end2 = start2 + 1
                    elif d2 == "TU":

                        if is_game(incompatible_pair[1]):
                            end2 = start2 + 1.5
                        else:
                            end2 = start2 + 2
                    else:
                        end2 = start2 + 2

                    # check for overlap in the time intervals
                    if max(start1, start2) < min(end1, end2):
                        return True

        # at this point no non-compatible pairs share the same slot
        return False

    def unwanted(self, schedule):
        for slot, event in schedule.scheduleVersion.items():
            for unwanted in self.input_parser.unwanted:
                if event != "$":
                    if unwanted["id"] == event.id and unwanted["day"] == slot.day and unwanted["time"] == slot.startTime:
                        return True
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

    # def check_overlapping(self, schedule):
    #     levels = ["U15", "U16", "U17", "U19"]
    #     tier_times = {}
    #     for slot in schedule.scheduleVersion.keys():
    #         if isinstance(slot, GameSlot):
    #             for game in slot.assignedGames:
    #                 u_level = game.tier[0:3]
    #                 if u_level in levels:
    #                     if game.tier in tier_times.keys():
    #                         if (slot.day, slot.startTime) in tier_times[game.tier]:
    #                             # overlap found, hard constraint failed
    #                             return True
    #                         else:
    #                             # keep track of times with U15/U16/U17/U19 games assigned to them
    #                             tier_times[game.tier].append((slot.day, slot.startTime))
    #                     else:
    #                         # keep track of tiers
    #                         tier_times[game.tier] = [(slot.day, slot.startTime)]

    #     return False

def is_game(id):
    if "PRC" in id.split() or "OPN" in id.split():
        return False
    else:
        return True
