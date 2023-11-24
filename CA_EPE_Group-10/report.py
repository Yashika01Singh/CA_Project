import numpy as np
import fileinput

routers = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8}
sources = {"0000": "A", "0100": "B", "1000": "C", "0001": "D",
                "0101": "E", "1001": "F", "0010": "G", "0110": "H", "1010": "I"}

def add_to_report(report,flits, clock):
    delays = []
    period = clock.cycle_period
    flag = clock.flag
    if flag == 'PVS':
        for line in fileinput.input(files='gaussian_delays.txt'):
            A = line.split(' ')
            new_value = []
            for value in A:
                if '\r' in value or '\n' in value:
                    value = float(value[0:len(value) - 1])
                    new_value.append(value)
                else:
                    value = float(value)
                    new_value.append(value)
            delays.append(new_value)
    else:
        for line in fileinput.input(files='delays.txt'):
            A = line.split(' ')
            new_value = []
            for value in A:
                if '\r' in value or '\n' in value:
                    value = float(value[0:len(value) - 1])
                    new_value.append(value)
                else:
                    value = float(value)
                    new_value.append(value)
            delays.append(new_value)

    for connection in flits.keys():
        report.write(f'{connection} : \n')
        messages = []
        for flit in flits[connection]:
            buff_delay = delays[routers[connection[0]]][0]
            if buff_delay <= period:
                buff_cycle = 1
            else:
                buff_cycle = 2
            sa_delay = delays[routers[connection[0]]][1]
            messages.append([f'\t Flit {flit[0]} : Received at t = {flit[1] * period} Sender: I/P Port Receiver: Buffer\n', flit[1] * period ])
            if sources[flits[connection][0][0][26:30]] == connection[0]:
                pass
            else:
                messages.append([f'\t Flit {flit[0]} : Received at t = {flit[1] * period + buff_delay} Sender: Buffer Receiver: SA\n', flit[1] * period + buff_delay])
                messages.append([f'\t Flit {flit[0]} : Received at t = {(flit[1] + buff_cycle) * period + sa_delay} Sender: SA Receiver: XBar\n', (flit[1] + buff_cycle) * period + sa_delay])
        messages.sort(key=lambda x: x[1])
        for m in messages:
            report.write(m[0])
        report.write(f'-----------------------------\n')


def generate_report_file(report, clock):
    file = open('Log.log', 'r')
    flits = {}
    for line in file:
        if 'Router' in line and 'Received' in line and 'from' in line:
            parts = line.split()
            sender = parts[1]
            receiver = parts[4]
            flit = parts[11]
            if f'{sender}-{receiver}' not in flits.keys() and receiver == 'PE':
                clock_cycle = int(parts[8])
                add_to_report(report, flits, clock)
                flits = {f'{sender}-{receiver}': [[flit, clock_cycle]]}
            elif f'{sender}-{receiver}' in flits.keys() and receiver == 'PE':
                clock_cycle = int(parts[8])
                flits[f'{sender}-{receiver}'].append([flit, clock_cycle])
            elif f'{sender}-{receiver}' not in flits.keys() and receiver != "Buffer" and receiver != "SA":
                clock_cycle = int(parts[8])
                flits[f'{sender}-{receiver}'] = [[flit, clock_cycle]]
            elif f'{sender}-{receiver}' in flits.keys() and receiver != "Buffer" and receiver != "SA":
                clock_cycle = int(parts[8])
                flits[f'{sender}-{receiver}'].append([flit, clock_cycle])
    add_to_report(report, flits, clock)


