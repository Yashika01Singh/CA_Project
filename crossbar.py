
class CrossBar:
    """
       0,0 : A
       0,1 : B
       0,2 : C
       1,0 : D
       1,1 : E
       1,2 : F
       2,0 : G
       2,1 : H
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
        # print(dest_router.XCurrent,dest_router.YCurrent)
        if self.moveData(dest_router, direction):
            self.currentConnected.append([dest_router, master, slave, direction])

    def sendFlit(self, master, flit):
        for i in self.currentConnected:
            if i[1] == master:
                if i[3] == "NORTH":
                    pos = i[0].buffer_shuffle(i[3])
                    i[0].north_buffer[pos] = flit
                if i[3] == "EAST":
                    pos = i[0].buffer_shuffle(i[3])
                    i[0].east_buffer[pos] = flit
                if i[3] == "WEST":
                    pos = i[0].buffer_shuffle(i[3])
                    i[0].west_buffer[pos] = flit
                if i[3] == "SOUTH":
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
            if dir == "NORTH":
                if next.isEmpty_north_buffer():
                    return True
            if dir == "EAST":
                if next.isEmpty_east_buffer():
                    return True
            if dir == "WEST":
                if next.isEmpty_west_buffer():
                    return True
            if dir == "SOUTH":
                if next.isEmpty_south_buffer():
                    return True
        return False

    def moveData(self, dest, dir):
        if self.checkNext(dest, dir):
            return True
