import numpy as np
import matplotlib.pyplot as plt
 

def read_for_link_graph(file_path):
    links = {'A-PE': 0, 'B-PE': 0, 'C-PE': 0, 'D-PE': 0, 'E-PE': 0, 'F-PE': 0, 'G-PE': 0, 'H-PE': 0, 'I-PE': 0,
             'A-B': 0, 'B-C': 0, 'C-F': 0, 'F-I': 0, 'I-H': 0, 'H-G': 0, 
             'G-D': 0, 'D-A': 0, 'B-E': 0, 'E-F': 0, 'E-H': 0, 'F-G': 0}

    with open(file_path, 'r') as file:
        for line in file:
            if 'Router' in line and 'Received' in line:
                parts = line.split()
                sender = parts[1]
                receiver = parts[4]
                link_key = f'{sender}-{receiver}'
                if link_key in links:
                    links[link_key] += 1

    return links


def read_for_latency_graph(file_path):
    pass

def plot_flits_sent(data):
    links = list(data.keys())
    flits_sent = list(data.values())

    plt.bar(links, flits_sent)
    plt.title(f'Number of Flits Sent')
    plt.xlabel('Link ID')
    plt.ylabel('Number of Flits Sent')
    plt.show()

def plot_latency(data):
    packets_sent = [entry[2] for entry in data]

    plt.plot(packets_sent, [entry[2] for entry in data], marker='o')
    plt.title(f'Packet Transfer Latency')
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
