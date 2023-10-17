class Packet:
    def __init__(self, Payload, Source, Destination, InjectCycleNum, PacketNum):
        self.Payload = Payload
        self.Source = Source
        self.Destination = Destination
        self.dict = {"A": "0000", "B": "0100", "C": "1000", "D": "0001",
                     "E": "0101", "F": "1001", "G": "0010", "H": "0110", "I": "1010"}
        self.InjectCycleNum = InjectCycleNum
        self.PacketNum = PacketNum

    def header(self):
        data = str(bin(self.PacketNum)[2:])
        length = 28 - len(data)
        return "0" * 11 + self.dict[self.Source] + "0" * 11 + self.dict[self.Destination] + "00"

    def tail(self):
        data = str(bin(self.PacketNum)[2:])
        length = 28 - len(data)
        return self.Payload[64:96]

    def body(self):
        return self.Payload[32:64]

    def flit(self):
        return [self.header(), self.body(), self.tail()]
