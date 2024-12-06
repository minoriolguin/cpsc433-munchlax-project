# CPSC 433 - Artificial Intelligence - Fall 2024
# Aditi Yadav
# Jaden Myers
# Minori Olguin
# Monica Nguyen
# Thi Ngoc Anh Nguyen

from input_parser import InputParser
from practiceSlot import PracticeSlot
from gameSlot import GameSlot

# function to check if all hard constraints are satisfied
def check_hard_constraints(schedule):
    # hard constraint 1
    if over_gamemax(schedule):
        return False

    # hard constraint 2
    if over_practicemax(schedule):
        return False

    # hard constraint 3
    if assign_equal():
        return False

    # hard constraint 4
    if notcompatable(schedule):
        return False

    # hard constraint 5
    if partassign():
        return False

    # hard constraint 6
    if unwanted():
        return False

    # city of calgary constraints:

    # city of calgary hard constraint 1
    if not_corresponding_games(): # check for both (monday, wednesday, friday) and (tuedsay, thursday)
        return False

    # city of calgary hard constraint 2
    if not_corresponding_practices(): # check for both (monday, wednesday) and (tuedsay, thursday)
        return False

    # city of calgary hard constraint 3
    if check_overlapping():
        return False

    # city of calgary hard constraint 4
    if check_meeting_time():
        return False

    # city of calgary hard constraint 5
    if check_special_practices():
        return False

    # at this point all the hard constraints have passed
    return True

def over_gamemax(schedule): # can probably be combined with over_practicemax
    for slot in schedule.scheduleVersion.keys():
         if isinstance(slot, GameSlot):
            if len(slot.assignedGames) > slot.gameMax:
                return True
    # at this point no game slot is over games max so this hard constraint passes
    return False

def over_practicemax(schedule):
    for slot in schedule.scheduleVersion.keys():
        if isinstance(slot, PracticeSlot):
            if len(slot.assignedPractices) > slot.pracMax:
                return True
        pass
    # at this point no practice slot is over practice max so this hard constraint passes
    return False

def assign_equal():
    pass

def notcompatable(schedule):
    # game_and_practice_slots = schedule.gameSlots + schedule.practiceSlots
    # for slot in game_and_practice_slots:

    #     # check that games/practices within the slot are compatable
    #     if isinstance(slot, PracticeSlot):
    #         for p1 in slot.assignPractices:
    #             for p2 in slot.assignPractices:
    #                 if p1 != p2:
                        pass
                        # how to check if compatable??

def partassign():
    pass

def unwanted():
    pass

def not_corresponding_games():
    pass

def not_corresponding_practices():
    pass

def check_overlapping():
    pass

def check_meeting_time():
    pass

def check_special_practices():
    pass
