# CPSC 433 - Artificial Intelligence - Fall 2024
# Aditi Yadav
# Jaden Myers
# Minori Olguin
# Monica Nguyen
# Thi Ngoc Anh Nguyen

from practiceSlot import PracticeSlot
from gameSlot import GameSlot
from scheduler import Schedule ## 

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
    
def over_gamemax(s: Schedule):
    for game_slot in s.games: # how will the games be accessed for an assignment
        if len(game_slot.assignedGames) > game_slot.gamesMax:
            return True
    
    # at this point no game slot is over games max so this hard constraint passes
    return False

def over_practicemax(s: Schedule):
    for practice_slot in s.games: # how will the practices be accessed for an assignment
        if len(practice_slot.assignedPractices) > practice_slot.pracMax:
            return True
    
    # at this point no practice slot is over practice max so this hard constraint passes
    return False

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
