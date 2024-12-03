class GameSlot:
    def __init__(self, rawLine):
        line = rawLine.split(',')
        self.id = rawLine
        self.day = line[0].strip()
        self.startTime = line[1].strip()
        self.gameMax = int(line[2].strip())
        self.gameMin = int(line[3].strip())
        # self.assignGames = []

    def __repr__(self):
        return f"GameSlot(day={self.day}, startTime={self.startTime}, gameMax={self.gameMax}, gameMin={self.gameMin})"
