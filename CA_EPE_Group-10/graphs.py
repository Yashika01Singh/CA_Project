import numpy as np
import matplotlib.pyplot as plt
 

def read_for_link_graph(file_path):
    links = {'A-PE': 0, 'B-PE': 0, 'C-PE': 0, 'D-PE': 0, 'E-PE': 0, 'F-PE': 0, 'G-PE': 0, 'H-PE': 0, 'I-PE': 0,
             'A-B': 0, 'B-C': 0, 'C-F': 0, 'F-I': 0, 'I-H': 0, 'H-G': 0, 
             'G-D': 0, 'D-A': 0, 'B-E': 0, 'E-F': 0, 'E-H': 0, 'F-G': 0}

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if 'Router' in line and 'Received' in line and 'from' in line:
                parts = line.split()
                sender = parts[1]
                receiver = parts[4]
                link_key = f'{sender}-{receiver}'
                link_key_1 = f'{receiver}-{sender}'
                if link_key in links:
                    links[link_key] += 1
                if link_key_1 in links:
                    links[link_key_1] += 1

    return links


def read_for_latency_graph(file_path):

    pkt_latency = {}

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if 'Router' in line and 'Received' in line and 'from' in line:
                parts = line.split()
                flit = parts[11]
                if (flit[-2:] == '01'):
                  if flit not in pkt_latency:
                    pkt_latency[flit] = [-1,0]

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if 'Router' in line and 'Received' in line and 'from' in line:
                parts = line.split()
                flit = parts[11]
                if (flit[-2:] == '01'):
                  if (pkt_latency[flit][0] == -1):
                    pkt_latency[flit][0] = parts[8]
                  else:
                    pkt_latency[flit][1] = parts[8]
                
    return pkt_latency

def plot_flits_sent(data):
    links = list(data.keys())
    flits_sent = list(data.values())

    plt.bar(links, flits_sent)
    plt.title(f'Number of Flits Sent')
    plt.xlabel('Link ID')
    plt.ylabel('Number of Flits Sent')
    plt.show()

def plot_latency(data):
    packets_sent = list(data.keys())
    cycles_taken = [int(array[1]) - int(array[0]) for array in data.values()]

    plt.bar(packets_sent, cycles_taken)
    plt.title('Packet Transfer Latency')
    plt.xlabel('Packets Sent')
    plt.ylabel('Latency (Clock Cycles)')
    plt.show()

def main():
    log_file_path = 'log.txt'

    data_link = read_for_link_graph(log_file_path)
    data_latency = read_for_latency_graph(log_file_path)

    plot_flits_sent(data_link)
    plot_latency(data_latency)

if __name__ == "__main__":
    main()
