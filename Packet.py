class Packet:
     def __init__(self,input):
          #create the required flit
          input = input.split(" ")
          self.source = int(input[1])
          self.destination = int(input[2])
          self.clockcycle = int(input[0])
          self.flitData = input[3]
     
     """def getflits(self):
          #return flits in a list like [head,body,tail]
          # and a flit should look like [clockcycle,source,destination,flitData]
          pass"""
     
     def getSource(self):
        return self.source
     
     def getDestination(self):
         return self.destination
     
     def getClockcycle(self):
         return self.clockcycle
     def getflit(self):
         return self.flitData
     
     

     