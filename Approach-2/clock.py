class Clock:
    def __init__(self, delays):
        self.cycle_count = 0
        self.cycle_value = 0
        self.cycle_period = self.calculate_period(delays)

    def startClock(self):
        self.cycle_value = 1
        self.cycle_count = 0

    def updateCycle(self):
        self.cycle_value = 0
        self.cycle_value += 1
        self.cycle_count += self.cycle_period

    def stopClock(self):
        self.cycle_count = 0
        self.cycle_value = 0

    def calculate_period(self, delays):
        max_delay = 0
        for router in delays:
            max_delay = max(router[0], router[1], router[2])

        int_delay = int(max_delay // 1)
        if max_delay - int_delay >= 0:
            int_delay += 1
        return int_delay
