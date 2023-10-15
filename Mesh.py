from Router import Router

class Mesh:
    def __init__(self):
        self.Mesh2D = []
        for i in range(9):  # Create 9 routers
            self.Mesh2D.append(Router(str(i)))
            
            for i in range(3):
                for j in range(3):
                    index = i * 3 + j
                    if j > 0:  # Connect to the left router
                        Router.LeftConnect(self.Mesh2D[index - 1],self.Mesh2D[index])
                    
                    if i > 0:  # Connect to the router above
                        Router.UpConnect(self.Mesh2D[index - 3],self.Mesh2D[index])

    def injectPacket(self,packet):
        source = packet.getSource()
        self.Mesh2D[source].RecievePacket("Local",packet)