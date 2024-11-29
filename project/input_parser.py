# CPSC 433 - Artificial Intelligence - Fall 2024
# Aditi Yadav
# Jaden Myers
# Minori Olguin
# Monica Nguyen
# Thi Ngoc Anh Nguyen

import sys

from gameSlot import GameSlot
from practiceSlot import PracticeSlot
from game import Game
from practice import Practice

class InputParser:
    
    def __init__(self):
        self.name = ''
        self.gameSlots = []
        self.practiceSlots = []
        self.games = []
        self.practices = []
        self.not_compatible = []
        self.unwanted = []
        self.preferences = []
        self.pair = []
        self.partial_assign = []
        self.filename = ''
        self.w_minfilled = 0
        self.w_pre = 0
        self.w_pair = 0
        self.w_secdiff = 0
        self.pen_gamemin = 0
        self.pen_practicemin = 0
        self.pen_notpaired = 0
        self.pen_section = 0

    def parse_argument(self):
        # Assume that all values have to specified
        if len(sys.argv) != 10:
            print("Usage: python main.py filename w_minfilled w_pref w_pair w_secdiff pen_gamemin pen_practicemin pen_notpaired pen_section")
            sys.exit(1)

        # Extract arguments from the command line
        # Assumption: all weights and penalties are integers (unsure as not specified in the problem)
        try:
            self.filename = sys.argv[1]
            self.wminfilled = int(sys.argv[2])
            self.wpref = int(sys.argv[3])
            self.wpair = int(sys.argv[4])
            self.wsecdiff = int(sys.argv[5])
            self.pengamemin = int(sys.argv[6])
            self.penpracticemin = int(sys.argv[7])
            self.pennotpaired = int(sys.argv[8])
            self.pensection = int(sys.argv[9])
        except ValueError:
            print("Error: weights and penalties must be integers")



    def parse_input_file(self):
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    line = line.strip()

                    # Skip empty lines
                    if not line:
                        continue

                    # Check if the line is a section header
                    if line.endswith(':'):
                        current_section = line[:-1]  
                        continue
                    
                    match current_section:
                        case 'Name':
                            self.name = line
                        case "Game slots":
                            self.gameSlots.append(GameSlot(line))
                        case "Practice slots":
                            self.practiceSlots.append(PracticeSlot(line))
                        case "Games":
                            self.games.append(Game(line))
                        case "Practices":
                            self.practices.append(Practice(line))
                        case "Not compatible":
                            self.not_compatible.append(self.splitLineByComma(line))
                        case "Unwanted":
                            self.unwanted.append(self.parseUnwanted_Partial(line))
                        case "Preferences":
                            self.preferences.append(self.parsePreference(line))
                        case "Pair":
                            self.pair.append(self.splitLineByComma(line))
                        case "Partial assignments":
                            self.partial_assign.append(self.parseUnwanted_Partial(line))
                            

        except FileNotFoundError:
            print(f"File '{self.filename}' not found.")
            sys.exit(1)

    def splitLineByComma(self, line):
        return [ele.strip() for ele in line.split(',')]

    def parseUnwanted_Partial(self, rawLine):
        line = [ele.strip() for ele in rawLine.split(',')]
        return{
            'id' : line[0],
            'day' : line[1],
            'time' : line[2],
        }
    
    def parsePreference(self, rawLine):
        line = [ele.strip() for ele in rawLine.split(',')]
        return{
            'day': line[0],
            'time': line[1],
            'id': line[2],
            'score': line[3]
        }

    def main(self):
        self.parse_argument()
        self.parse_input_file()

        ## ------ DEBUG ------ ##
        print(self.name)
        # print(self.gameSlots)
        # print(self.gameSlots[0].day)
        # print(self.practiceSlots)
        # print(self.games)
        # print(self.practices)
        # print(self.not_compatible)
        # print(self.unwanted)
        # print(self.preferences)
        # print(self.pair)
        # print(self.partial_assign)



