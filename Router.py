from Buffers import Buffers
import logging
from Clock import Clock
logging.basicConfig(filename="Logfile.log", filemode='a')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
import threading
class Port:

    def __init__(self):
        self.NorthInput = False
        self.NorthOutput = False
        self.SouthInput = False
        self.SouthOutput = False
        self.EastInput = False
        self.EastOutput = False
        self.WestInput = False
        self.WestOutput = False
        self.Local = False

    def make_connection(self, DirectionFrom, DirectionTo):
        if (DirectionFrom == "North"):
            self.NorthInput = True
        elif (DirectionFrom == "South"):
            self.SouthInput = True
        elif (DirectionFrom == "East"):
            self.EastInput = True
        elif (DirectionFrom == "West"):
            self.WestInput = True
        elif (DirectionFrom == "Local"):
            self.Local = True

        if (DirectionTo == "North"):
            self.NorthOutput = True
        elif (DirectionTo == "South"):
            self.SouthOutput = True
        elif (DirectionTo == "East"):
            self.EastOutput = True
        elif (DirectionTo == "West"):
            self.WestOutput = True
        elif (DirectionTo == "Local"):
            self.Local = True

    def break_connection(self, DirectionFrom, DirectionTo):
        if (DirectionFrom == "North"):
            self.NorthInput = False
        elif (DirectionFrom == "South"):
            self.SouthInput = False
        elif (DirectionFrom == "East"):
            self.EastInput = False
        elif (DirectionFrom == "West"):
            self.WestInput = False
        elif (DirectionTo == "Local"):
            self.Local = False

        if (DirectionTo == "North"):
            self.NorthOutput = False
        elif (DirectionTo == "South"):
            self.SouthOutput = False
        elif (DirectionTo == "East"):
            self.EastOutput = False
        elif (DirectionTo == "West"):
            self.WestOutput = False
        elif (DirectionTo == "Local"):
            self.Local = False

    

class Router:

    def __init__(self, name, sa_delay, xbar_delay, buffer_delay):
        self.name = name
        self.NorthConnection = None
        self.SouthConnection = None
        self.EastConnection = None
        self.WestConnection = None
        self.LocalConnection = None
        self.buffers = Buffers()
        self.ports = Port()

        self.sa_delay = sa_delay
        self.xbar_delay = xbar_delay
        self.buffer_delay = buffer_delay

        self.clockPeriod = None
        self.clockFrequency = None

    def Add_Connection(self, Direction, NextRouter):
        if (Direction == "North"):
            self.NorthConnection = NextRouter
        if (Direction == "South"):
            self.SouthConnection = NextRouter
        if (Direction == "East"):
            self.EastConnection = NextRouter
        if (Direction == "West"):
            self.WestConnection = NextRouter
        if (Direction == "Local"):
            self.LocalCOnnection = NextRouter

    def print_info(self):
        print(f"Router Name: {self.name}")
        if self.NorthConnection:
            print(f"  North Connection: {self.NorthConnection.name}")
        if self.SouthConnection:
            print(f"  South Connection: {self.SouthConnection.name}")
        if self.EastConnection:
            print(f"  East Connection: {self.EastConnection.name}")
        if self.WestConnection:
            print(f"  West Connection: {self.WestConnection.name}")

    def LeftConnect(LeftRouter, RightRouter):
        LeftRouter.Add_Connection("East", RightRouter)
        RightRouter.Add_Connection("West", LeftRouter)

    def UpConnect(UpRouter, DownRouter):
        UpRouter.Add_Connection("South", DownRouter)
        DownRouter.Add_Connection("North", UpRouter)

    def send_packet_in_thread(self,NextRouter, NextDirection, packet, clk):
        NextRouter.RecievePacket(NextDirection, packet, clk)

    def CrossBar(self, DirectionFrom, DirectionTo ,packet,clk):

        if (DirectionTo == "East"):
            NextRouter = self.EastConnection
            NextDirection = "West"
        elif (DirectionTo == "West"):
            NextRouter = self.WestConnection
            NextDirection = "East"
        elif (DirectionTo == "North"):
            NextRouter = self.NorthConnection
            NextDirection = "South"
        elif (DirectionTo =="South"):
            NextRouter = self.SouthConnection
            NextDirection = "North"

        self.ports.make_connection(DirectionFrom, DirectionTo)
        
        
        packet_thread = threading.Thread(target=self.send_packet_in_thread, args=(NextRouter,NextDirection, packet, clk))
        clk.update()
        packet_thread.start()
        self.ports.break_connection(DirectionFrom, DirectionFrom)

    def SwitchAllocator(self, Direction,clk):
        packet = self.buffers.remove(Direction)
        current_x, current_y = self.name%3 , self.name//3
        Destination = packet.getDestination()
        destination_x, destination_y = Destination%3 , Destination//3
        NextDirection = ""
        if(current_x<destination_x):
            NextDirection = "East"
        elif (current_x>destination_x):
            NextDirection = "West"
        else :
            if(current_y < destination_y):
                NextDirection = "South"
            else:
                NextDirection = "North"


        self.CrossBar ( Direction , NextDirection , packet,clk)
        # Figure out which connection to send to
        # store that connection in Next Connection
        # Use XBar to do that
        

    def RecievePacket(self, Direction, packet , clk):
        # the packet is stored in PE buffer
        # call the switch allocator to see which connection to be used
        # use the crossbar to send to the output port in that direction
        # packet recieved at input of next
        logger.info('Router: ' + str(self.name) + ' at clock cycle ' + str(clk.value()) +' Flit received: ' + packet.getflit())
        if (packet.getDestination() == self.name):
            return True
        self.buffers.insert(Direction, packet)
        self.SwitchAllocator(Direction,clk)
        

    # def DefineDelays(self, sa, xbar, buffer):
    #     self.sa_delay = sa
    #     self.xbar_delay = xbar
    #     self.buffer_delay = buffer

    def CalculateClockValues(self):
        self.clockPeriod = max(self.sa_delay, self.xbar_delay, self.buffer_delay)
        self.clockFrequency = 1/self.clockPeriod

