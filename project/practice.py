class Practice:
    def __init__(self, rawLine):
        line = rawLine.split(' ')
        self.id = rawLine
        self.league = line[0]
        self.tier = line[1]
        self.div = ''
        self.type = ''
        self.index = 0
        for i in range (2, len(line)):
            if line[i] == 'DIV':
                self.div = int(line[i+1])
                i += 1
                continue
            elif line[i] == 'PRC':
                self.type = 'PRC'
                self.index = int(line[i+1])
            elif line[i] == 'OPN':
                self.type = 'OPN'
                self.index = int(line[i+1])
            

    def __repr__(self):
        return f"Practice(league={self.league} tier={self.tier} div={self.div} type={self.type} index={self.index})"