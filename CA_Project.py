
# 0 --- 1 --- 2 
# |     |     |     
# 3 --- 4 --- 5 
# |     |     |     
# 6 --- 7 --- 8 


from Router import Router
from Packet import Packet
from Mesh import Mesh
from Clock import Clock
    
def main():
    
   
    input = []

    with open('traffic.txt', 'r') as file:
       
        for line in file:
            
            packet = Packet(line)
            input.append(packet)
    #possible sort the input so that clock cycles are ..
    myMesh = Mesh()
    clk = Clock()
    
    for i in range(len(input)):
        
        #do the time stuff here
        success = myMesh.injectPacket(input[i],clk)
        
    

if __name__ == "__main__":
  main()