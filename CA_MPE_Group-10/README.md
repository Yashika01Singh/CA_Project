# CSE511 Group Project

# Designing a Cycle Accurate Simulator for Network-on-Chip (NoC) router and mesh with provision to study the impact of Process Variations

## MPE Deliverables
1. Your simulator must read and interpret the traffic file.
2. Your simulator must be able to read and interpret the delays file.
3. Your simulator must also support at least one of the routing algorithms.
4. Your simulator must also be able to inject packets as per the traffic file.
5. A working simulator that can generate the log file for at least PVA mode.
6. A working simulator that can generate the report file for at least PVA mode.
7. The log file should include the cycle count and the flits received in that cycle.

## Description 
Input of traffic file is taken from the file called "traffic.txt" that specifies which packets are put in the NoC at which clock cycle. A 3x3 NoC Mesh is instantiated that contanins 9 routers with each router having 5 ports. XY Routing has been implemented. We have created a log file called "log.log" to log the status and specifies what happens throughout each clock cycle. Delays are being read from file called "delays.txt". Report file is also being generated.   

## How to run code

To run the code, you need to have a working python environment.

Step-1: Clone the repo from GitHub using the command:

```git clone https://github.com/Yashika01Singh/CA_Project```

Step-2: Create a new python environment (if it does not exist):

```python3 -m venv myenv```

Step-3: Now, activate the python environment using the following code:

(For macOS)

```source myenv/bin/activate```

Step-4: After activating the environment, navigate to the folder containing the code.

Step-5: Run the following script to get the output for Log file in 'Log.log'. You might not be seeing the report file. This will be generated after you press Ctrl+C on your terminal to flush the written item to the file.

```python3 main.py -t traffic.txt -r XY -d delays.txt```

Here,
-t - Flag for input traffic file

-d - Flag for input delay file

-r - Routing Algorithm (XY or YX)







## Group Members 
1. Aanya Trehan (aanya20419@iiitd.ac.in)
2. Apoorva Arya (apoorva20032@iiitd.ac.in)
3. Jayan Pahuja (jayan20071@iiitd.ac.in)
4. Yashika Singh (yashika20161@iiitd.ac.in)
