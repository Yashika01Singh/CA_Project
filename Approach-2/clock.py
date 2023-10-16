class Clock:
    def __init__(self):
        self.cycle_count = 0
        self.cycle_value = 0

    def startClock(self):
        self.cycle_value = 1
        self.cycle_count = 1

    def updateCycle(self):
        self.cycle_value = 0
        self.cycle_value = 1
        self.cycle_count += 1

    def stopClock(self):
        self.cycle_count = 0
        self.cycle_value = 0
