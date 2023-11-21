from port import Port
from crossbar import CrossBar
from processing_entity import PE
from send import Send

import logging

logging.basicConfig(filename="Log.log", filemode='a')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
class Router:

    def __init__(self, X, Y, clock, delays):

        self.send = None
        self.neighbour_dict = []
        self.XCoordinate = X
        self.YCoordinate = Y
        self.crossbar = CrossBar()
        self.pe = PE
        self.send_flag = 0
        self.clock = clock
        self.delays = delays

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
        self.neighbour_list = []
        self.ports_list = []


        self.dict = {'00': 'A', '10': 'B', '20': 'C', '01': 'D',
                     '11': 'E', '21': 'F', '02': 'G', '12': 'H', '22': 'I'}
        self.cycles = []

        self.makePEPorts()
        self.process_cycles()

    def makePEPorts(self):
        port_per = Port()
        self.pe.input_port = port_per
        self.pe_output_port = port_per
        port_per.setPort(self.pe.input_port, self.pe_output_port)

        port_rpe = Port()
        self.pe_input_port = port_rpe
        self.pe.output_port = port_rpe
        port_rpe.setPort(self.pe_output_port, self.pe.input_port)

    def switchAllocator(self, Xdest, Ydest, flag):
        if flag == 'XY':
            Xoffset = int(Xdest) - self.XCoordinate
            Yoffset = int(Ydest) - self.YCoordinate
            if Xoffset < 0:
                return self.XCoordinate - 1, self.YCoordinate
            elif Xoffset > 0:
                return self.XCoordinate + 1, self.YCoordinate
            elif Xoffset == 0 and Yoffset < 0:
                return self.XCoordinate, self.YCoordinate - 1
            elif Xoffset == 0 and Yoffset > 0:
                return self.XCoordinate, self.YCoordinate + 1
        elif flag == 'YX':
            Xoffset = int(Xdest) - self.XCoordinate
            Yoffset = int(Ydest) - self.YCoordinate
            if Yoffset < 0:
                return self.XCoordinate, self.YCoordinate - 1
            elif Yoffset > 0:
                return self.XCoordinate, self.YCoordinate + 1
            elif Yoffset == 0 and Xoffset < 0:
                return self.XCoordinate - 1, self.YCoordinate
            elif Yoffset == 0 and Xoffset > 0:
                return self.XCoordinate + 1, self.YCoordinate

    def process_cycles(self):
        for delay in self.delays:
            if delay <= self.clock.cycle_period:
                self.cycles.append(1)
            else:
                self.cycles.append(2)

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

    def buffer_shuffle(self, direction):
        if direction == "North":
            for i in range(0, 4):
                if self.north_buffer[i] == "0" * 32:
                    return i
        elif direction == "South":
            for i in range(0, 4):
                if self.south_buffer[i] == "0" * 32:
                    return i
        elif direction == "East":
            for i in range(0, 4):
                if self.east_buffer[i] == "0" * 32:
                    return i
        elif direction == "West":
            for i in range(0, 4):
                if self.west_buffer[i] == "0" * 32:
                    return i
        elif direction == "PE":
            for i in range(0, 4):
                if self.pe_buffer[i] == "0" * 32:
                    return i
    
    def update(self, clock, flag):
        if self.send_flag == 1:
        
            self.send.send(clock)
            if self.send.count == 3:
                self.send_flag = 0
                return -1
            return 1
        elif not self.isEmpty_pe_buffer():
            print("PE")
            self.lastbuffer = self.pe_buffer
            self.send = Send(self, self.pe_buffer, 'PE', flag)
            self.pe_buffer = ["0" * 32] * 3
            self.send_flag = 1
            return 1

        elif not self.isEmpty_west_buffer():
            print("West")
            self.lastbuffer=self.west_buffer
            self.send = Send(self, self.west_buffer, 'West', flag)
            self.west_buffer = ["0" * 32] * 3
            self.send_flag = 1
            return 1

        elif not self.isEmpty_north_buffer():
            print("North")
            self.lastbuffer=self.north_buffer
            self.send = Send(self, self.north_buffer, 'North', flag)
            self.north_buffer = ["0" * 32] * 3
            self.send_flag = 1
            return 1

        elif not self.isEmpty_east_buffer():
            print("East")
            self.lastbuffer=self.east_buffer
            self.send = Send(self, self.east_buffer, 'East', flag)
            self.east_buffer = ["0" * 32] * 3
            self.send_flag = 1
            return 1

        elif not self.isEmpty_south_buffer():
            print("South")
            self.lastbuffer =  self.south_buffer
            self.send = Send(self, self.south_buffer, 'South', flag)
            self.south_buffer = ["0" * 32] * 3
            self.send_flag = 1
            return 1
        return 0
