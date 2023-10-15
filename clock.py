class Clock:
    def __init__(self):
        self.cycle_count = 0
        self.cycle_value = 0

    def start_clock(self):
        self.cycle_value = 1
        self.cycle_count = 1

    def update_cycle(self):
        self.cycle_value = 0
        self.cycle_value = 1
        self.cycle_count += 1

    def stop_clock(self):
        self.cycle_count = 0
        self.cycle_value = 0
