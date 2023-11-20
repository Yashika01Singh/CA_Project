import logging

logging.basicConfig(filename="Log.log", filemode='a')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Send:
    def __init__(self, Router, buffer, direction, flag):
        self.count = 0
        self.buffer = buffer
        self.router = Router
        self.router_send = None
        self.dict = {'00': 'A', '10': 'B', '20': 'C', '01': 'D',
                     '11': 'E', '21': 'F', '02': 'G', '12': 'H', '22': 'I'}
        self.direction_buffer_dict = {"East": self.router.east_buffer,
                                      "West": self.router.west_buffer,
                                      "North": self.router.north_buffer,
                                      "South": self.router.south_buffer,
                                      "PE": self.router.pe_buffer}
        self.directions = direction
        self.report_file = open('report.txt', 'a')
        self.calculateReceiver(flag)

    def calculateReceiver(self, flag):
        if self.router.XCoordinate == int(self.buffer[0][26] + self.buffer[0][27],2) and self.router.YCoordinate == int(self.buffer[0][28] + self.buffer[0][29],2):
            if self.router is not None:
                self.direction_buffer_dict[self.directions] = ["0" * 32] * 3

        else:
            moveX, moveY = self.router.switchAllocator(int(self.buffer[0][26] + self.buffer[0][27], 2),int(self.buffer[0][28] + self.buffer[0][29], 2), flag)
            if self.router.neighbour_list[0].XCoordinate == moveX and self.router.neighbour_list[0].YCoordinate == moveY:
                self.router_send = self.router.neighbour_list[0]
            elif self.router.neighbour_list[1].XCoordinate == moveX and self.router.neighbour_list[1].YCoordinate == moveY:
                self.router_send = self.router.neighbour_list[1]
            elif len(self.router.neighbour_list) == 3:
                if self.router.neighbour_list[2].XCoordinate == moveX and self.router.neighbour_list[2].YCoordinate == moveY:
                    self.router_send = self.router.neighbour_list[2]
            elif len(self.router.neighbour_list) == 4:
                if self.router.neighbour_list[2].XCoordinate == moveX and self.router.neighbour_list[2].YCoordinate == moveY:
                    self.router_send = self.router.neighbour_list[2]
                if self.router.neighbour_list[3].XCoordinate == moveX and self.router.neighbour_list[3].YCoordinate == moveY:
                    self.router_send = self.router.neighbour_list[3]

            if moveX == self.router.XCoordinate - 1:
                self.directions = "West"
            elif moveX == self.router.XCoordinate + 1:
                self.directions = "East"
            elif moveY == self.router.YCoordinate - 1:
                self.directions = "North"
            elif moveY == self.router.YCoordinate + 1:
                self.directions = "South"

    def send(self, clock):
        self.report_file = open('report.txt', 'a')
        if self.router_send is not None:
            # print(str(self.router_send.XCoordinate) + " " + str(self.router.YCoordinate))
            route = self.dict[str(self.router_send.XCoordinate) + str(self.router_send.YCoordinate)]
            route_self = self.dict[str(self.router.XCoordinate) + str(self.router.YCoordinate)]
            print(route + " " + route_self)
            logger.info('Router: ' + route + " Received from " + route_self + " at clock cycle: " + str(
                clock.cycle_count) + ' Flit received: ' + self.buffer[self.count] + 'Received At: Buffer of Router: ' + route)
            self.report_file.write('Reporter Info: \n Router: ' + route + " Received from " + route_self + " at a delay of: " + str(
                3*clock.cycle_period) + ' Flit received: ' + self.buffer[self.count] + "\n")
            self.report_file.flush()
            if self.directions == "North":
                self.router_send.north_buffer[self.count] = self.buffer[self.count]
            elif self.directions == "West":
                self.router_send.west_buffer[self.count] = self.buffer[self.count]
            elif self.directions == "South":
                self.router_send.south_buffer[self.count] = self.buffer[self.count]
            elif self.directions == "East":
                self.router_send.east_buffer[self.count] = self.buffer[self.count]
        self.count += 1
        self.report_file.close()
