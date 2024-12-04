class PracticeSlot:
    def __init__(self, rawLine):
        line = rawLine.split(',')
        self.id = rawLine
        self.day = line[0].strip()
        self.startTime = line[1].strip()
        self.pracMax = int(line[2].strip())
        self.pracMin = int(line[3].strip())
        self.assignPractices = []
        
    def is_full(self):
        return len(self.assignPractices) >= self.pracMax
    
    def __repr__(self):
        return f"PracticeSlot(day={self.day}, startTime={self.startTime}, pracMax={self.pracMax}, pracMin={self.pracMin})"