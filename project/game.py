# CPSC 433 - Artificial Intelligence - Fall 2024
# Aditi Yadav
# Jaden Myers
# Minori Olguin
# Monica Nguyen
# Thi Ngoc Anh Nguyen

class Game:
    def __init__(self, rawLine):
        line = rawLine.split(' ')
        self.id = rawLine
        self.league = line[0]
        self.tier = line[1]
        self.div = int(line[3])

    def __repr__(self):
        return f"Game(league={self.league} tier={self.tier} div={self.div})"
