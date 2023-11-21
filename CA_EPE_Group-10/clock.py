import numpy as np


class Clock:
    def __init__(self, delays, logger, flag):
        self.logger = logger
        self.cycle_count = 0
        self.cycle_value = 0
        self.cycle_period = self.calculate_period(delays, flag)
        self.time = 0
        self.logger.info("Clock is starting.\n")

    def startClock(self):
        self.cycle_value = 1
        self.cycle_count = 1
        self.time = 0

    def updateCycle(self):
        self.cycle_value = 1
        self.cycle_count += 1
        self.time += self.cycle_period

    def stopClock(self):
        self.cycle_count = 0
        self.cycle_value = 0

    def calculate_period(self, delays, flag):
        file = open('gaussian_delays.txt', 'w')
        if flag == 'PVS':
            max_delay = 0
            for router in delays:
                x = np.random.normal(loc=router[0], scale=router[0] / 10)
                y = np.random.normal(loc=router[1], scale=router[1] / 10)
                z = np.random.normal(loc=router[2], scale=router[2] / 10)
                max_delay = max(router[0], router[1], router[2])
                ans = (0.7 * router[0] <= x <= 1.3 * router[0]) and (0.7 * router[1] <= y <= 1.3 * router[1]) and (
                        0.7 * router[2] <= z <= 1.3 * router[2])
                self.logger.info(msg=f'Delay for Buffer => {x}')
                self.logger.info(msg=f'Delay for Switch Allocator (SA) => {y}')
                self.logger.info(msg=f'Delay for X-Bar => {z}')
                self.logger.info(msg=f'Delay is in the limit (mean - 3*sigma, mean + 3*sigma) => {ans}')
                file.write(f'{x} {y} {z}\n')

        else:
            max_delay = 0
            for router in delays:
                x = router[0]
                y = router[1]
                z = router[2]
                max_delay = max(x, y, z)
                self.logger.info(msg=f'Delay for Buffer => {x}')
                self.logger.info(msg=f'Delay for Switch Allocator (SA) => {y}')
                self.logger.info(msg=f'Delay for X-Bar => {z}')
                file.write(f'{x} {y} {z}\n')

        print(max_delay)
        int_delay = int(max_delay // 1)
        if max_delay - int_delay > 0:
            int_delay += 1
        file.close()
        self.logger.info(msg=f'Clock Period is: {int_delay}')
        return int_delay
