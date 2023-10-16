class Packet:
    def __init__(self, Payload, Source, Destination, InjectCycleNum, PacketNum):
        self.Payload = Payload
        self.Source = Source
        self.Destination = Destination
        self.InjectCycleNum = InjectCycleNum
        self.PacketNum = PacketNum

    def header(self):
        data = str(bin(self.PacketNum)[2:])
        length = 28 - len(data)
        return self.Payload[0:32]

    def tail(self):
        data = str(bin(self.PacketNum)[2:])
        length = 28 - len(data)
        return self.Payload[64:96]

    def body(self):
        return self.Payload[32:64]

    def flit(self):
        return [self.header(), self.body(), self.tail()]

