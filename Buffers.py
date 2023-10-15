class Buffers:

    def __init__(self):
        self.PeBuffer = []
        self.NorthBuffer = []
        self.SouthBuffer = []
        self.EastBuffer = []
        self.WestBuffer = []

    def insert(self , direction , flit):
        if(direction == "Local"):
            self.PeBuffer.append(flit)

        if(direction == "North"):
            self.NorthBuffer.append(flit)

        if(direction == "South"):
            self.SouthBuffer.append(flit)
        
        if(direction == "East"):
            self.EastBuffer.append(flit)
        
        if(direction == "West"):
            self.WestBuffer.append(flit)

    def remove(self, direction):

        if(direction == "Local"):
            flit = self.PeBuffer.pop()

        if(direction == "North"):
            flit = self.NorthBuffer.pop()

        if(direction == "South"):
            flit =self.SouthBuffer.pop()

        if(direction == "East"):
           flit =  self.EastBuffer.pop()
        
        if(direction == "West"):
            flit = self.WestBuffer.pop()

        return flit