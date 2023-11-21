import fileinput
import numpy as np
import matplotlib.pyplot as plt
 

def read_for_link_graph(file_path):
    pass

def read_for_latency_graph(file_path):
    pass

def plot_flits_sent(data):
    links = [entry[0] for entry in data]
    flits_sent = [entry[1] for entry in data]

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
