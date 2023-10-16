import logging

logging.basicConfig(filename="Logfile.log", filemode='a')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class Send:
    def __init__(self, Router, buffer, direction, flag):
        # print('helo')
        self.count = 0
        self.buffer = buffer
        self.router = Router
        self.router_send = None
        self.dict = {'00': 'A', '01': 'B', '02': 'C', '10': 'D',
                     '11': 'E', '12': 'F', '20': 'G', '21': 'H', '22': 'I'}
        self.directions = direction
        self.calculateReceiver(flag)

    def calculateReceiver(self, flag):
        # print('bufer',self.buffer)
        if self.router.XCurrent == int(self.buffer[0][28]) and self.router.YCurrent == int(self.buffer[0][29]):
            # print("halo\n")
            # print(self.router.XCurrent, self.router.YCurrent, self.router.north_buffer, self.router.south_buffer, self.router.east_buffer, self.router.west_buffer)
            if self.router is not None:
                if self.directions == "North":
                    self.router.north_buffer = ["0" * 32] * 3
                elif self.directions == "West":
                    self.router.west_buffer = ["0" * 32] * 3
                elif self.directions == "South":
                    self.router.south_buffer = ["0" * 32] * 3
                elif self.directions == "East":
                    self.router.east_buffer = ["0" * 32] * 3
                elif self.directions == "PE":
                    self.router.pe_buffer = ["0" * 32] * 3

        else:
            moveX, moveY = self.router.switchAllocator(self.buffer[0][28], self.buffer[0][29], flag)
            if self.router.neighbour_list[0].XCurrent == moveX and self.router.neighbour_list[0].YCurrent == moveY:
                self.router_send = self.router.neighbour_list[0]
            if self.router.neighbour_list[1].XCurrent == moveX and self.router.neighbour_list[1].YCurrent == moveY:
                self.router_send = self.router.neighbour_list[1]
            # print('yo',moveX,moveY)
            if moveX == self.router.XCurrent - 1:
                self.directions = "South"
            elif moveX == self.router.XCurrent + 1:
                self.directions = "North"
            elif moveY == self.router.YCurrent - 1:
                self.directions = "East"
            elif moveY == self.router.YCurrent + 1:
                self.directions = "West"

    def send(self, clock):
        if self.router_send is not None:
            route = self.dict[str(self.router_send.XCurrent) + str(self.router_send.YCurrent)]
            route_self = self.dict[str(self.router.XCurrent) + str(self.router.YCurrent)]
            logger.info('Router: ' + route + " Received from " + route_self + " at clock cycle: " + str(
                clock) + ' Flit received: ' + self.buffer[self.count])
            if self.directions == "North":
                self.router_send.north_buffer[self.count] = self.buffer[self.count]
                # print(self.router_send.north_buffer[self.count])
            elif self.directions == "West":
                self.router_send.west_buffer[self.count] = self.buffer[self.count]
                # print('west',self.router_send.west_buffer[self.count])
            elif self.directions == "South":
                self.router_send.south_buffer[self.count] = self.buffer[self.count]
                # print(self.router_send.south_buffer[self.count])
            elif self.directions == "East":
                self.router_send.east_buffer[self.count] = self.buffer[self.count]
                # print(self.router_send.east_buffer[self.count])
        self.count += 1
