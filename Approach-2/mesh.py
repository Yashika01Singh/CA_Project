from router import Router
from port import Port


# A --- B --- C
# |     |     |
# D --- E --- F
# |     |     |
# G --- H --- I

class Mesh:
    def __init__(self):
        self.router_a = Router(0, 0)
        self.router_b = Router(1, 0)
        self.router_c = Router(2, 0)
        self.router_d = Router(0, 1)
        self.router_e = Router(1, 1)
        self.router_f = Router(2, 1)
        self.router_g = Router(0, 2)
        self.router_h = Router(1, 2)
        self.router_i = Router(2, 2)

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
        a = self.router_a.update(clock, flag)
        b = self.router_b.update(clock, flag)
        c = self.router_c.update(clock, flag)
        d = self.router_d.update(clock, flag)
        e = self.router_e.update(clock, flag)
        f = self.router_f.update(clock, flag)
        g = self.router_g.update(clock, flag)
        h = self.router_h.update(clock, flag)
        i = self.router_i.update(clock, flag)
        return a + b + c + d + e + f + g + h + i

    def injectPacket(self, flit, count, source):
        if source == 'A':
            self.router_a.pe_buffer[count] = flit
        elif source == 'B':
            self.router_b.pe_buffer[count] = flit
        elif source == 'C':
            self.router_c.pe_buffer[count] = flit
        elif source == 'D':
            self.router_d.pe_buffer[count] = flit
        elif source == 'E':
            self.router_e.pe_buffer[count] = flit
        elif source == 'F':
            self.router_f.pe_buffer[count] = flit
        elif source == 'G':
            self.router_g.pe_buffer[count] = flit
        elif source == 'H':
            self.router_h.pe_buffer[count] = flit
        elif source == 'I':
            self.router_i.pe_buffer[count] = flit
        return 1
