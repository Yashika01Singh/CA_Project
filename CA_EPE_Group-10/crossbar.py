class CrossBar:
   
    def CrossBar(self, DirectionFrom, DirectionTo ,packet):

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
        NextRouter.RecievePacket(NextDirection, packet)

        self.ports.break_connection(DirectionFrom, DirectionFrom)