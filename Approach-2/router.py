from port import Port
from crossbar import CrossBar
from processing_entity import PE
from send import Send


class Router:
    # 5 ports (input and output)
    # Class Ports
    # input connected Output Connected
    # processing element dummy class
    # class crossbar (connects input and output port)

    def __init__(self, X, Y):

        self.neighbour_dict = []
        self.XCurrent = X
        self.YCurrent = Y
        self.crossbar = CrossBar()
        self.pe = PE
        self.send_flag = 0

        self.north_input_port = None
        self.south_input_port = None
        self.east_input_port = None
        self.west_input_port = None
        self.pe_input_port = None

        self.north_output_port = None
        self.south_output_port = None
        self.east_output_port = None
        self.west_output_port = None
        self.pe_output_port = None

        self.north_buffer = ["0" * 32] * 3
        self.south_buffer = ["0" * 32] * 3
        self.east_buffer = ["0" * 32] * 3
        self.west_buffer = ["0" * 32] * 3
        self.pe_buffer = ["0" * 32] * 3

        port_pr = Port()
        self.pe.input_port = port_pr
        self.pe_output_port = port_pr
        port_pr.setPort(self.pe.input_port, self.pe_output_port)

        port_rp = Port()
        self.pe_input_port = port_rp
        self.pe.output_port = port_rp
        port_rp.setPort(self.pe_input_port, self.pe.input_port)
        self.neighbour_list = []
        self.ports_list = []

    def switchAllocator(self, Xdest, Ydest, flag):
        if flag == 'YX':
            Xoffset = int(Xdest) - self.XCurrent
            Yoffset = int(Ydest) - self.YCurrent
            if Xoffset < 0:
                return self.XCurrent - 1, self.YCurrent
            if Xoffset > 0:
                return self.XCurrent + 1, self.YCurrent
            if Xoffset == 0 and Yoffset < 0:
                return self.XCurrent, self.YCurrent - 1
            if Xoffset == 0 and Yoffset > 0:
                return self.XCurrent, self.YCurrent + 1
        elif flag == 'XY':
            Xoffset = int(Xdest) - self.XCurrent
            Yoffset = int(Ydest) - self.YCurrent
            if Yoffset < 0:
                return self.XCurrent, self.YCurrent - 1
            if Yoffset > 0:
                return self.XCurrent, self.YCurrent + 1
            if Yoffset == 0 and Xoffset < 0:
                return self.XCurrent - 1, self.YCurrent
            if Yoffset == 0 and Xoffset > 0:
                return self.XCurrent + 1, self.YCurrent

    # def ifChannel(self, Xoff, Yoff):
    #     if Xoff == 0 and Yoff == 0:
    #         self.channel = "idk"  # internal

    def isEmpty_north_buffer(self):
        for i in self.north_buffer:
            if i == '0' * 32:
                return True
        return False

    def isEmpty_south_buffer(self):
        for i in self.south_buffer:
            if i == '0' * 32:
                return True
        return False

    def isEmpty_east_buffer(self):
        for i in self.east_buffer:
            if i == '0' * 32:
                return True
        return False

    def isEmpty_west_buffer(self):
        for i in self.west_buffer:
            if i == '0' * 32:
                return True
        return False

    def isEmpty_pe_buffer(self):
        for i in self.pe_buffer:
            if i == '0' * 32:
                return True
        return False

    # def checker(self,router,dir):
    #     if(dir=="NORTH"):
    #         return router.isempty_north_buffer()
    #     elif(dir=="SOUTH"):
    #         return router.isempty_south_buffer()
    #     elif(dir=="EAST"):
    #         return router.isempty_east_buffer()
    #     elif(dir=="WEST"):
    #         return router.isempty_west_buffer()

    def shiftNBuffer(self):
        for i in range(0, 9):
            self.north_buffer[i] = self.north_buffer[i + 1]

        self.north_buffer[9] = "0" * 32

    def shiftSBuffer(self):
        for i in range(0, 9):
            self.south_buffer[i] = self.south_buffer[i + 1]

        self.south_buffer[9] = "0" * 32

    def shiftEBuffer(self):
        for i in range(0, 9):
            self.east_buffer[i] = self.east_buffer[i + 1]

        self.east_buffer[9] = "0" * 32

    def shiftWBuffer(self):
        for i in range(0, 9):
            self.west_buffer[i] = self.west_buffer[i + 1]

        self.west_buffer[9] = "0" * 32

    def shiftPEBuffer(self):
        for i in range(0, 9):
            self.pe_buffer[i] = self.pe_buffer[i + 1]

        self.pe_buffer[9] = "0" * 32

    def buffer_shuffle(self, dir):
        if dir == "North":
            for i in range(0, 4):
                if self.north_buffer[i] == "0" * 32:
                    return i
        elif dir == "South":
            for i in range(0, 4):
                if self.south_buffer[i] == "0" * 32:
                    return i
        elif dir == "East":
            for i in range(0, 4):
                if self.east_buffer[i] == "0" * 32:
                    return i
        elif dir == "West":
            for i in range(0, 4):
                if self.west_buffer[i] == "0" * 32:
                    return i
        elif dir == "PE":
            for i in range(0, 4):
                if self.pe_buffer[i] == "0" * 32:
                    return i

    def update(self, clock, flag):
        if self.send_flag == 1:
            # print('count',self.send.count)
            self.send.send(clock)
            if self.send.count == 3:
                # print('done', self.XCurrent, self.YCurrent)
                self.send_flag = 0
                return -1
            return 1
        elif not self.isEmpty_pe_buffer():
            # print('1')
            self.send = Send(self, self.pe_buffer, 'PE', flag)
            self.pe_buffer = ["0" * 32] * 3
            self.send_flag = 1
            return 1

        elif not self.isEmpty_west_buffer():
            # print('2')
            self.send = Send(self, self.west_buffer, 'West', flag)
            self.west_buffer = ["0" * 32] * 3
            self.send_flag = 1
            return 1

        elif not self.isEmpty_north_buffer():
            # print('3')
            self.send = Send(self, self.north_buffer, 'North', flag)
            self.north_buffer = ["0" * 32] * 3
            self.send_flag = 1
            return 1

        elif not self.isEmpty_east_buffer():
            # print('4')
            self.send = Send(self, self.east_buffer, 'East', flag)
            self.east_buffer = ["0" * 32] * 3
            self.send_flag = 1
            return 1

        elif not self.isEmpty_south_buffer():
            # print('5')
            self.send = Send(self, self.south_buffer, 'South', flag)
            self.south_buffer = ["0" * 32] * 3
            self.send_flag = 1
            return 1
        return 0
        # print('empty',self.XCurrent,self.YCurrent)

        # if self.isempty_pe_buffer()==True:
        #     self.startRouting('PE')
        # if self.isempty_east_buffer() == False:
        #     self.startRouting('EAST')
        # if self.isempty_north_buffer() == False:
        #     self.startRouting('NORTH')
        # if self.isempty_south_buffer() == False:
        #     self.startRouting('SOUTH')

        # self.startRouting('WEST')

        # if self.isempty_pe_buffer() == False:
        #     self.startRouting('PE')

    def startRouting(self, dir):

        if dir == 'North':
            if self.north_buffer[0][32:] == '0' * 2:
                moveX, moveY = self.switchAllocator(self.north_buffer[0][28:30][0], self.north_buffer[0][28:30][1])
                router_send = None
                if self.neighbour_list[0].XCurrent == moveX and self.neighbour_list[0].YCurrent == moveY:
                    router_send = self.neighbour_list[0]
                if self.neighbour_list[1].XCurrent == moveX and self.neighbour_list[1].YCurrent == moveY:
                    router_send = self.neighbour_list[1]
                if moveX == self.XCurrent - 1:
                    self.crossbar.makeConnection(router_send, self.north_input_port, self.north_output_port, "South")
                elif moveX == self.XCurrent + 1:
                    self.crossbar.makeConnection(router_send, self.north_input_port, self.south_output_port, "North")
                elif moveY == self.YCurrent - 1:
                    self.crossbar.makeConnection(router_send, self.north_input_port, self.west_output_port, "East")
                elif moveY == self.YCurrent + 1:
                    self.crossbar.makeConnection(router_send, self.north_input_port, self.east_output_port, "West")
                self.crossbar.sendFlit(self.north_input_port, self.north_buffer[0])
                self.shiftNBuffer()

            if self.north_buffer[0][32:] == '01':
                self.crossbar.sendFlit(self.north_input_port, self.north_buffer[0])
                self.shiftNBuffer()

            if self.north_buffer[0][32:] == '11':
                self.crossbar.sendFlit(self.north_input_port, self.north_buffer[0])
                self.shiftNBuffer()
                self.crossbar.deleteConnection(self.north_input_port)

        if dir == 'PE':
            if self.pe_buffer[0][32:] == '0' * 2:
                moveX, moveY = self.switchAllocator(self.pe_buffer[0][28:30][0], self.pe_buffer[0][28:30][1])
                router_send = None
                if self.neighbour_list[0].XCurrent == moveX and self.neighbour_list[0].YCurrent == moveY:
                    router_send = self.neighbour_list[0]
                if self.neighbour_list[1].XCurrent == moveX and self.neighbour_list[1].YCurrent == moveY:
                    router_send = self.neighbour_list[1]
                if moveX == self.XCurrent - 1:
                    self.crossbar.makeConnection(router_send, self.pe_input_port, self.north_output_port, "South")
                elif moveX == self.XCurrent + 1:
                    self.crossbar.makeConnection(router_send, self.pe_input_port, self.south_output_port, "North")
                elif moveY == self.YCurrent - 1:
                    self.crossbar.makeConnection(router_send, self.pe_input_port, self.west_output_port, "East")
                elif moveY == self.YCurrent + 1:
                    self.crossbar.makeConnection(router_send, self.pe_input_port, self.east_output_port, "West")
                self.crossbar.sendFlit(self.pe_input_port, self.pe_buffer[0])
                self.shiftPEBuffer()

            if self.pe_buffer[0][32:] == '01':
                self.crossbar.sendFlit(self.pe_input_port, self.pe_buffer[0])
                self.shiftPEBuffer()

            if self.pe_buffer[0][32:] == '11':
                self.crossbar.sendFlit(self.pe_input_port, self.pe_buffer[0])
                self.shiftPEBuffer()
                self.crossbar.deleteConnection(self.pe_input_port)

        if dir == 'South':
            if self.south_buffer[0][32:] == '0' * 2:
                moveX, moveY = self.switchAllocator(self.south_buffer[0][28:30][0], self.south_buffer[0][28:30][1])
                router_send = None
                if self.neighbour_list[0].XCurrent == moveX and self.neighbour_list[0].YCurrent == moveY:
                    router_send = self.neighbour_list[0]
                if self.neighbour_list[1].XCurrent == moveX and self.neighbour_list[1].YCurrent == moveY:
                    router_send = self.neighbour_list[1]
                if moveX == self.XCurrent - 1:
                    self.crossbar.makeConnection(router_send, self.south_input_port, self.north_output_port, "South")
                elif moveX == self.XCurrent + 1:
                    self.crossbar.makeConnection(router_send, self.south_input_port, self.south_output_port, "North")
                elif moveY == self.YCurrent - 1:
                    self.crossbar.makeConnection(router_send, self.south_input_port, self.west_output_port, "East")
                elif moveY == self.YCurrent + 1:
                    self.crossbar.makeConnection(router_send, self.south_input_port, self.east_output_port, "West")
                self.crossbar.sendFlit(self.south_input_port, self.south_buffer[0])
                self.shiftSBuffer()

            if self.south_buffer[0][32:] == '01':
                self.crossbar.sendFlit(self.south_input_port, self.south_buffer[0])
                self.shiftSBuffer()

            if self.south_buffer[0][32:] == '11':
                self.crossbar.sendFlit(self.south_input_port, self.south_buffer[0])
                self.shiftSBuffer()
                self.crossbar.deleteConnection(self.south_input_port)

        if dir == 'East':
            if self.east_buffer[0][32:] == '0' * 2:
                moveX, moveY = self.switchAllocator(self.east_buffer[0][28:30][0], self.east_buffer[0][28:30][1])
                router_send = None
                if self.neighbour_list[0].XCurrent == moveX and self.neighbour_list[0].YCurrent == moveY:
                    router_send = self.neighbour_list[0]
                if self.neighbour_list[1].XCurrent == moveX and self.neighbour_list[1].YCurrent == moveY:
                    router_send = self.neighbour_list[1]
                if moveX == self.XCurrent - 1:
                    self.crossbar.makeConnection(router_send, self.east_input_port, self.north_output_port, "South")
                elif moveX == self.XCurrent + 1:
                    self.crossbar.makeConnection(router_send, self.east_input_port, self.south_output_port, "North")
                elif moveY == self.YCurrent - 1:
                    self.crossbar.makeConnection(router_send, self.east_input_port, self.west_output_port, "East")
                elif moveY == self.YCurrent + 1:
                    self.crossbar.makeConnection(router_send, self.east_input_port, self.east_output_port, "West")
                self.crossbar.sendFlit(self.east_input_port, self.east_buffer[0])
                self.shiftEBuffer()

            if self.east_buffer[0][32:] == '01':
                self.crossbar.sendFlit(self.east_input_port, self.east_buffer[0])
                self.shiftEBuffer()

            if self.east_buffer[0][32:] == '11':
                self.crossbar.sendFlit(self.east_input_port, self.east_buffer[0])
                self.shiftEBuffer()
                self.crossbar.deleteConnection(self.east_input_port)

        if dir == 'West':
            if self.west_buffer[0][32:] == '0' * 2:
                moveX, moveY = self.switchAllocator(self.west_buffer[0][28:30][0], self.west_buffer[0][28:30][1])
                router_send = None
                if self.neighbour_list[0].XCurrent == moveX and self.neighbour_list[0].YCurrent == moveY:
                    router_send = self.neighbour_list[0]
                if self.neighbour_list[1].XCurrent == moveX and self.neighbour_list[1].YCurrent == moveY:
                    router_send = self.neighbour_list[1]
                if moveX == self.XCurrent - 1:
                    self.crossbar.makeConnection(router_send, self.west_input_port, self.north_output_port, "South")
                elif moveX == self.XCurrent + 1:
                    self.crossbar.makeConnection(router_send, self.west_input_port, self.south_output_port, "North")
                elif moveY == self.YCurrent - 1:
                    self.crossbar.makeConnection(router_send, self.west_input_port, self.west_output_port, "East")
                elif moveY == self.YCurrent + 1:
                    self.crossbar.makeConnection(router_send, self.west_input_port, self.east_output_port, "West")
                self.crossbar.sendFlit(self.west_input_port, self.west_buffer[0])
                self.shiftWBuffer()

            if self.west_buffer[0][32:] == '01':
                self.crossbar.sendFlit(self.west_input_port, self.west_buffer[0])
                self.shiftWBuffer()

            if self.west_buffer[0][32:] == '11':
                self.crossbar.sendFlit(self.west_input_port, self.west_buffer[0])
                self.shiftWBuffer()
                self.crossbar.deleteConnection(self.west_input_port)
