from router import Router
from port import Port
import fileinput


# A --- B --- C
# |     |     |
# D --- E --- F
# |     |     |
# G --- H --- I

class Mesh:
    def __init__(self, clock):

        f = open('gaussian_delays.txt', 'r')
        delays = []
        for line in f.readlines():
            A = line.split(' ')
            print(A)
            new_value = []
            for value in A:
                if '\r' in value or '\n' in value:
                    value = float(value[0:len(value) - 1])
                    new_value.append(value)
                else:
                    value = float(value)
                    new_value.append(value)
            delays.append(new_value)

        print(delays)

        self.router_a = Router(0, 0, clock, delays[0])
        self.router_b = Router(1, 0, clock, delays[1])
        self.router_c = Router(2, 0, clock, delays[2])
        self.router_d = Router(0, 1, clock, delays[3])
        self.router_e = Router(1, 1, clock, delays[4])
        self.router_f = Router(2, 1, clock, delays[5])
        self.router_g = Router(0, 2, clock, delays[6])
        self.router_h = Router(1, 2, clock, delays[7])
        self.router_i = Router(2, 2, clock, delays[8])

        self.router_a.neighbour_dict = [{self.router_b: "East"}, {self.router_d: "South"}]
        self.router_a.neighbour_list = [self.router_b, self.router_d]
        self.router_b.neighbour_dict = [{self.router_a: "West"}, {self.router_c: "East"}, {self.router_e: "South"}]
        self.router_b.neighbour_list = [self.router_a, self.router_c, self.router_e]
        self.router_c.neighbour_dict = [{self.router_b: "West"}, {self.router_f: "South"}]
        self.router_c.neighbour_list = [self.router_b, self.router_f]
        self.router_d.neighbour_dict = [{self.router_a: "North"}, {self.router_g: "South"}, {self.router_e: "East"}]
        self.router_d.neighbour_list = [self.router_a, self.router_g, self.router_e]
        self.router_e.neighbour_dict = [{self.router_b: "North"}, {self.router_d: "West"}, {self.router_h: "South"},
                                        {self.router_f: "East"}]
        self.router_e.neighbour_list = [self.router_b, self.router_d, self.router_h, self.router_f]
        self.router_f.neighbour_dict = [{self.router_e: "West"}, {self.router_c: "North"}, {self.router_i: "South"}]
        self.router_f.neighbour_list = [self.router_e, self.router_c, self.router_i]
        self.router_g.neighbour_dict = [{self.router_d: "North"}, {self.router_h: "East"}]
        self.router_g.neighbour_list = [self.router_h, self.router_d]
        self.router_h.neighbour_dict = [{self.router_i: "East"}, {self.router_g: "West"}, {self.router_e: "North"}]
        self.router_h.neighbour_list = [self.router_i, self.router_g, self.router_e]
        self.router_i.neighbour_dict = [{self.router_f: "North"}, {self.router_h: "West"}]
        self.router_i.neighbour_list = [self.router_f, self.router_h]

        self.routers_list = [self.router_a, self.router_b, self.router_c, self.router_d, self.router_e,
                             self.router_f, self.router_g, self.router_h, self.router_i]

        self.definePorts()
        self.sources_dict = {'A': self.router_a, 'B': self.router_b, 'C': self.router_c,
                             'D': self.router_d, 'E': self.router_e, 'F': self.router_f,
                             'G': self.router_g, 'H': self.router_h, 'I': self.router_i}

    def definePorts(self):
        for router in self.routers_list:
            router.ports_list = []
            for neighbour in router.neighbour_dict:
                source_router = router
                dest_router = list(neighbour.keys())[0]
                direction = neighbour[dest_router]

                port_xy = Port()
                if direction == "East":
                    source_router.east_input_port = port_xy
                    dest_router.west_output_port = port_xy
                elif direction == "West":
                    source_router.west_input_port = port_xy
                    dest_router.east_output_port = port_xy
                elif direction == "North":
                    source_router.north_input_port = port_xy
                    dest_router.south_output_port = port_xy
                elif direction == "South":
                    source_router.south_input_port = port_xy
                    dest_router.north_output_port = port_xy
                port_xy.setPort(source_router, dest_router)
                router.ports_list.append(port_xy)

    def update(self, clock, flag):
        total = 0
        for key in self.sources_dict.keys():
            total += self.sources_dict[key].update(clock, flag)
        return total

    def injectPacket(self, flit, count, source):
        self.sources_dict[source].pe_buffer[count] = flit
        return 1
