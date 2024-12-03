# CPSC 433 - Artificial Intelligence - Fall 2024
# Aditi Yadav
# Jaden Myers
# Minori Olguin
# Monica Nguyen
# Thi Ngoc Anh Nguyen

from practiceSlot import PracticeSlot
from gameSlot import GameSlot

# function to check if all hard constraints are satisfied
def check_hard_constraints():
    # hard constraint 1
    if over_gamemax():
        return False
    
    # hard constraint 2
    if over_practicemax():
        return False
    
    # hard constraint 3
    if assign_equal():
        return False
    
    # hard constraint 4
    if notcompatable():
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
    if check_special_prectices():
        return False

    # at this point all the hard constraints have passed
    return True
    
def over_gamemax(slot: GameSlot):
    pass

def over_practicemax(slot: PracticeSlot):
    pass

def assign_equal():
    pass

def notcompatable():
    pass

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

def check_special_prectices():
    pass
