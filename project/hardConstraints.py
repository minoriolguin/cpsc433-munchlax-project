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
def check_hard_constraints(schedule: InputParser):
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
    if notcompatible():
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
    
    if evening_divisions():
        return False

    # at this point all the hard constraints have passed
    return True
    
def over_gamemax(schedule: InputParser):
    for game_slot in schedule.gameSlots:
        if len(game_slot.assignGames) > game_slot.gameMax:
            return True
    
    # at this point no game slot is over games max so this hard constraint passes
    return False

def over_practicemax(schedule: InputParser):
    for practice_slot in schedule.practiceSlots:
        if len(practice_slot.assignPractices) > practice_slot.pracMax:
            return True
    
    # at this point no practice slot is over practice max so this hard constraint passes
    return False

def assign_equal(schedule: InputParser):
    for slot in schedule.slots:
        games = slot.assignGames
        practices = slot.assignPractices

        # check for overlap in divisions
        game_divisions = set(game.div for game in games)
        practice_divisions = set(practice.div for practice in practices)

        # check if theres any common division
        if game_divisions.intersection(practice_divisions):
            return True  # constraint violated because an overlap between practices and games is found
    return False 

def notcompatible(schedule: InputParser):
    # combine all the slots into a single list
    all_slots = schedule.gameSlots + schedule.practiceSlots

    # check each non compatible pair
    for event_a, event_b in schedule.not_compatible:
        # check if both the events are assigned to the same slot
        if any( (event_a in slot.assignGames + slot.assignPractices) and (event_b in slot.assignGames + slot.assignPractices)
            for slot in all_slots):
            return True  # constraint violated

    # at this point no not-compatible pairs share the same slot
    return False

def partassign(schedule: InputParser):
    
    for partial_assg in schedule.partial_assign:
        event, assigned_slot = partial_assg[0], partial_assg[1]

        # check to skip if assigned slot is the placeholder - "$"
        if assigned_slot == "$":
            continue
        
        for slot in schedule.gameSlots + schedule.practiceSlots:
            if slot == assigned_slot:
                if event not in slot.assignGames and event not in slot.assignPractices:
                    return True
    return False


def unwanted(schedule: InputParser):
    # go through all the unwanted constraints
    for unwanted_constraints in schedule.unwanted:
        event, unwanted_slot = unwanted_constraints[0], unwanted_constraints[1]

    # check if event is assigned to unwanted slot
    for slot in schedule.gameSlots + schedule.practiceSlots:
        if slot == unwanted_slot:
            if event in slot.assignGames or event in slot.assignPractices:
                return True # constraint violated
    return False

def not_corresponding_games(): # this function isn't needed? combine mon, wed, fri slots in input parser?
    pass

def not_corresponding_practices():
    pass

def evening_divisions(schedule: InputParser):
    for gameSlot in schedule.gameSlots:
        for game in gameSlot.games:
            if str(game.div)[0] == "9" and int(str(gameSlot.startTime)[0:2]) < 12:
                return True
    
    return False

def check_overlapping():
    pass

def check_meeting_time():
    pass

def check_special_practices():
    pass
