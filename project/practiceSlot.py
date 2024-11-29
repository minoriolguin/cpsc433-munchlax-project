class PracticeSlot:
    def __init__(self, line):
        self.day = line[0]
        self.startTime = line[1]
        self.pracMax = int(line[2])
        self.pracMin = int(line[3])
        self.assignPractices = []

    def __repr__(self):
        return f"PracticeSlot(day={self.day}, startTime={self.startTime}, pracMax={self.pracMax}, pracMin={self.pracMin})"