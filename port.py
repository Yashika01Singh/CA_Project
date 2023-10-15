from clock import Clock


class Port:
    def __init__(self):
        self.unused_port = 1
        self.input_edge = None
        self.output_edge = None

    def set_port(self, input_port, output_port):
        self.input_edge = input_port
        self.output_edge = output_port
