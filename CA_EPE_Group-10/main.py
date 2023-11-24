import argparse
import fileinput
import logging
import signal
import sys
from clock import Clock
from mesh import Mesh
import report


parser = argparse.ArgumentParser()
parser.add_argument("-t", "--traffic", help="Traffic File as Input")
parser.add_argument("-d", "--delay", help="Input Delay File")
parser.add_argument("-r", "--routing", help="Routing Algorithm you want to use")
parser.add_argument("-s", "--simulation", help="Simulation Mode you want to use")
args = parser.parse_args()

logging.basicConfig(filename="Log.log", filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

delays = []
for line in fileinput.input(files=args.delay):
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

open('Log.log', 'w').close()
flag = args.simulation
clk = Clock(delays, logger, flag)


def sig_handler(sig, frame):
    logger.info("Simulation has ended.")
    print('\nEnd of Simulation')
    f = open('report.txt','w')
    report.generate_report_file(f,clk)
    sys.exit(0)


signal.signal(signal.SIGINT, sig_handler)


input_data = []
processed = []
counter = 0

def process_line(line):
    fields = line.split()
    result = fields[:3]
    last_field = fields[3]
    chunks = [last_field[i:i+32] for i in range(0, len(last_field), 32)]
    result.extend(chunks)
    return result

with open(args.traffic, 'r') as file:
        for line in file:
            # Process each line and append the result to the final list
            processed.append(process_line(line.strip()))


clk.startClock()
Mesh3D = Mesh(clk)

# Main simulation loop
current_input_index = 0
flit_received = 0  # Flag to track flit reception
print(processed)
print("Start of Simulation")
messages = []
while True:
    if current_input_index < len(processed) and int(processed[current_input_index][0]) <= clk.cycle_count:
        flit_index = 3
        max_flit = 6
        while flit_index < max_flit:
            flit_received = 0  # Reset the flit reception flag
            if processed[current_input_index][flit_index] != "0" * 32:
                flit_received = Mesh3D.injectPacket(processed[current_input_index][flit_index], flit_index - 3,
                                                    processed[current_input_index][1])
                if flit_received == 1:
                    log_message = (
                        f'Router: {processed[current_input_index][1]} Received from PE at clock cycle: {clk.cycle_count} '
                        f'Flit received: {processed[current_input_index][flit_index]} Received At: Buffer of Router: {processed[current_input_index][1]}'
                    )#Logging the messages
                    logger.info(log_message)

                    messages.append(['Router: ' + processed[current_input_index][1] + " Received from " + "Buffer" + " at clock cycle: " + str(
                        clk.cycle_count + Mesh3D.sources_dict[processed[current_input_index][1]].cycles[1]) + ' Flit received: ' + processed[current_input_index][flit_index] + ' Received At: SA of Router: ' + processed[current_input_index][1], clk.cycle_count + Mesh3D.sources_dict[processed[current_input_index][1]].cycles[1]])
                    messages.append(['Router: ' + processed[current_input_index][1] + " Received from " + "SA" + " at clock cycle: " + str(
                        clk.cycle_count + Mesh3D.sources_dict[processed[current_input_index][1]].cycles[1] + Mesh3D.sources_dict[processed[current_input_index][1]].cycles[2]) + ' Flit received: ' + processed[current_input_index][flit_index] + ' Received At: XBar of Router: ' + processed[current_input_index][1], clk.cycle_count + Mesh3D.sources_dict[processed[current_input_index][1]].cycles[1] + Mesh3D.sources_dict[processed[current_input_index][1]].cycles[2]])
                    for message in messages:
                        print(message, clk.cycle_count)
                        if message[1] <= clk.cycle_count:
                            print("In Loop")
                            logger.info(message[0])
                            messages.remove(message)

                    processed[current_input_index][flit_index] = "0" * 32
                    flit_received = 1
                    break
                else:
                    break
            elif processed[current_input_index][max_flit - 1] == "0" * 32:
                print(messages)
                for message in messages:
                    logger.info(message[0])

                if len(messages) != 0:
                    for i in range(0, messages[-1][1] - clk.cycle_count + 1):
                        clk.updateCycle()

                messages = []
                current_input_index += 1
                break
            flit_index += 1
    value = Mesh3D.update(clk, args.routing)
    if value >= 0:
        clk.updateCycle()
