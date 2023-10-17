from Router import Router


class Mesh:
    def __init__(self):
        self.Mesh2D = []

        with open('delays.txt', 'r') as delayFile:
            delayData = delayFile.readlines()

        # for i in range(9):  # Create 9 routers
        i1 = 0
        while i1 < 9:  # Create 9 routers
            RouterDelay = delayData[i1].strip().split()
            sa_delay = float(RouterDelay[0])
            xbar_delay = float(RouterDelay[1])
            buffer_delay = float(RouterDelay[2])
            self.Mesh2D.append(
                Router(i1, sa_delay, xbar_delay, buffer_delay))
            Router.CalculateClockValues(self.Mesh2D[i1])
            i1 = i1+1

        for i in range(3):
            for j in range(3):
                index = i * 3 + j
                if j > 0:  # Connect to the left router
                    Router.LeftConnect(
                        self.Mesh2D[index - 1], self.Mesh2D[index])

                if i > 0:  # Connect to the router above
                    Router.UpConnect(
                        self.Mesh2D[index - 3], self.Mesh2D[index])

    def injectPacket(self, packet):
        
        source = packet.getSource()
        self.Mesh2D[source].RecievePacket("Local", packet)
        
        return True