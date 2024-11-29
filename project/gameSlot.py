class GameSlot:
    def __init__(self, line):
        self.day = line[0]
        self.startTime = line[1]
        self.gameMax = int(line[2])
        self.gameMin = int(line[3])
        self.assignGames = []

    def __repr__(self):
        return f"GameSlot(day={self.day}, startTime={self.startTime}, gameMax={self.gameMax}, gameMin={self.gameMin})"
