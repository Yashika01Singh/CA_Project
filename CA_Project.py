
# 0 --- 1 --- 2 
# |     |     |     
# 3 --- 4 --- 5 
# |     |     |     
# 6 --- 7 --- 8 



class PE:
    pass

def LeftConnect(LeftRouter , RightRouter):
    LeftRouter.Add_Connection("East",RightRouter)
    RightRouter.Add_Connection("West",LeftRouter)

def UpConnect(UpRouter , DownRouter):
    UpRouter.Add_Connection("South",DownRouter)
    DownRouter.Add_Connection("North",UpRouter)
    
class Router:

    def __init__(self,name):
        self.name = name
        self.NorthConnection = None
        self.SouthConnection = None
        self.EastConnection = None
        self.WestConnection = None

    def Add_Connection(self,Direction,NextRouter):
        if(Direction=="North"):
            self.NorthConnection = NextRouter
        if(Direction=="South"):
            self.SouthConnection = NextRouter
        if(Direction=="East"):
            self.EastConnection = NextRouter
        if(Direction=="West"):
            self.WestConnection = NextRouter
        
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

class SwitchAllocator:
    pass

def CreateMesh():
    Mesh = []
    for i in range(9):  # Create 9 routers
        Mesh.append(Router(str(i)))
    
    for i in range(3):
        for j in range(3):
            index = i * 3 + j
            if j > 0:  # Connect to the left router
                LeftConnect(Mesh[index - 1],Mesh[index])
               
            if i > 0:  # Connect to the router above
                UpConnect(Mesh[index - 3],Mesh[index])

    return Mesh


    
def main():
    Mesh = CreateMesh()
    for router in Mesh:
        router.print_info()
    

if __name__ == "__main__":
  main()