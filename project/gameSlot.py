class GameSlot:
    def __init__(self, rawLine):
        line = rawLine.split(',')
        self.id = rawLine
        self.day = line[0].strip()
        self.startTime = line[1].strip()
        self.gameMax = int(line[2].strip())
        self.gameMin = int(line[3].strip())
        self.assignedGames = []

    def is_full(self):
        return len(self.assignedGames) >= self.gameMax

    def remaining_capacity(self):
        return self.gameMax - len(self.assignedGames)

    def copy(self):
        copied_slot = GameSlot(self.id)
        copied_slot.day = self.day
        copied_slot.startTime = self.startTime
        copied_slot.gameMax = self.gameMax
        copied_slot.gameMin = self.gameMin
        copied_slot.assignedGames = self.assignedGames[:]
        return copied_slot

    def __repr__(self):
        return f"GameSlot(day={self.day}, startTime={self.startTime}, gameMax={self.gameMax}, gameMin={self.gameMin})"
