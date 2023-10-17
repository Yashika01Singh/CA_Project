class Clock:

    def __init__(self):
        self.cycle_count = 0

    def update(self):
        self.cycle_count += 1

    def value(self):
        return self.cycle_count
