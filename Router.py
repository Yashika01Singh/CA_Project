from Buffers import Buffers


class Router:

    def __init__(self, name, sa_delay, xbar_delay, buffer_delay):
        self.name = name
        self.NorthConnection = None
        self.SouthConnection = None
        self.EastConnection = None
        self.WestConnection = None
        self.LocalConnection = None
        self.buffers = Buffers()

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
    def CrossBar(self,DirectionFrom , DirectionTo ,packet):
        
        self.NextRouter.RecievePacket(NextDirection, packet)
        pass
    def SwitchAllocator(self, Direction):
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


        self.CrossBar ( self , Direction , NextDirection , packet)
        # Figure out which connection to send to
        # store that connection in Next Connection
        # Use XBar to do that
        

    def RecievePacket(self, Direction, packet):
        # the packet is stored in PE buffer
        # call the switch allocator to see which connection to be used
        # use the crossbar to send to the output port in that direction
        # packet recieved at input of next
        if (packet.getDestinantion() == self.name):
            # log the packet
            pass
        self.buffers.insert(Direction, packet)
        self.SwitchAllocator(Direction)

    # def DefineDelays(self, sa, xbar, buffer):
    #     self.sa_delay = sa
    #     self.xbar_delay = xbar
    #     self.buffer_delay = buffer

    def CalculateClockValues(self):
        self.clockPeriod = max(self.sa_delay, self.xbar_delay, self.buffer_delay)
        self.clockFrequency = 1/self.clockPeriod
