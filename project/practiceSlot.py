class PracticeSlot:
    def __init__(self, rawLine):
        line = rawLine.split(',')
        self.id = rawLine
        self.day = line[0].strip()
        self.startTime = line[1].strip()
        self.pracMax = int(line[2].strip())
        self.pracMin = int(line[3].strip())
        self.assignedPractices = []

    def is_full(self):
        return len(self.assignedPractices) >= self.pracMax

    def copy(self):
        copied_slot = PracticeSlot(self.id)
        copied_slot.day = self.day
        copied_slot.startTime = self.startTime
        copied_slot.pracMax = self.pracMax
        copied_slot.pracMin = self.pracMin
        copied_slot.assignedPractices = self.assignedPractices[:]
        return copied_slot

    def __repr__(self):
        return f"PracticeSlot(day={self.day}, startTime={self.startTime}, pracMax={self.pracMax}, pracMin={self.pracMin})"
