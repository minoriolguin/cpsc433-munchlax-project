# CPSC 433 - Artificial Intelligence - Fall 2024
# Aditi Yadav
# Jaden Myers
# Minori Olguin
# Monica Nguyen
# Thi Ngoc Anh Nguyen

import sys
import os

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
            sys.exit()

        for i in range (2, len(sys.argv)):
            if not sys.argv[i].isnumeric():
                print("Usage: w_minfilled w_pref w_pair w_secdiff pen_gamemin pen_practicemin pen_notpaired pen_section are numbers")
                sys.exit()

        # Extract arguments from the command line
        self.filename = sys.argv[1]
        self.wminfilled = int(sys.argv[2])
        self.wpref = int(sys.argv[3])
        self.wpair = int(sys.argv[4])
        self.wsecdiff = int(sys.argv[5])
        self.pengamemin = int(sys.argv[6])
        self.penpracticemin = int(sys.argv[7])
        self.pennotpaired = int(sys.argv[8])
        self.pensection = int(sys.argv[9])


    def parse_input_file(self):
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                current_section = None

                for i in range (len(lines)):
                    line = lines[i]
                    line = line.strip()

                    # Skip empty lines
                    if not line:
                        continue
                    
                    # print(line)

                    # Check if the line is a section header
                    if line.endswith(':'):
                        current_section = line[:-1]  
                        continue
                    
                    if current_section == 'Name':
                        self.name = line
                        continue


                    lineArr = line.split(',')
                    match current_section:
                        case "Game slots":
                            self.gameSlots.append(lineArr)
                        case "Practice slots":
                            self.practiceSlots.append(lineArr)
                        case "Games":
                            self.games.append(lineArr)
                        case "Practices":
                            self.practices.append(lineArr)
                        case "Not compatible":
                            self.not_compatible.append(lineArr)
                        case "Unwanted":
                            self.unwanted.append(lineArr)
                        case "Preferences":
                            self.preferences.append(lineArr)
                        case "Pair":
                            self.pair.append(lineArr)
                        case "Partial assignments":
                            self.partial_assign.append(lineArr)
                            

        except FileNotFoundError:
            print(f"Input file '{self.filename}' not found.")
            sys.exit(1)


    def main(self):
        self.parse_argument()
        self.parse_input_file()

        print(self.name)
        print(self.gameSlots)
        print(self.practiceSlots)
        print(self.games)
        print(self.practiceSlots)
        print(self.not_compatible)
        print(self.unwanted)
        print(self.preferences)
        print(self.pair)
        print(self.partial_assign)



