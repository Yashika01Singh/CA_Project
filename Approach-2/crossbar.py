
class CrossBar:
    """
       0,0 : A
       1,0 : B
       2,0 : C
       0,1 : D
       1,1 : E
       2,1 : F
       0,2 : G
       1,2 : H
       2,2 : I
       """

    def __init__(self):
        # self.northI = northI
        # self.southI = southI
        # self.westI = westI
        # self.eastI = eastI
        # self.northO = northO
        # self.southO = southO
        # self.westO = westO
        # self.eastO = eastO
        self.currentConnected = []

    def makeConnection(self, dest_router, master, slave, direction):
        print("Making connection")
        # print(dest_router.XCoordinate,dest_router.YCoordinate)
        if self.moveData(dest_router, direction):
            self.currentConnected.append([dest_router, master, slave, direction])

    def sendFlit(self, master, flit):
        for i in self.currentConnected:
            if i[1] == master:
                if i[3] == "North":
                    pos = i[0].buffer_shuffle(i[3])
                    i[0].north_buffer[pos] = flit
                if i[3] == "East":
                    pos = i[0].buffer_shuffle(i[3])
                    i[0].east_buffer[pos] = flit
                if i[3] == "West":
                    pos = i[0].buffer_shuffle(i[3])
                    i[0].west_buffer[pos] = flit
                if i[3] == "South":
                    pos = i[0].buffer_shuffle(i[3])
                    i[0].south_buffer[pos] = flit

    def deleteConnection(self, master):
        for i in self.currentConnected:
            if i[1] == master:
                self.currentConnected.remove(i)

    def checkNext(self, next, dir):
        if next == None:
            pass
        # if next is empty so data is shifted
        else:
            if dir == "North":
                if next.isEmpty_north_buffer():
                    return True
            if dir == "East":
                if next.isEmpty_east_buffer():
                    return True
            if dir == "West":
                if next.isEmpty_west_buffer():
                    return True
            if dir == "South":
                if next.isEmpty_south_buffer():
                    return True
        return False

    def moveData(self, dest, dir):
        if self.checkNext(dest, dir):
            return True
