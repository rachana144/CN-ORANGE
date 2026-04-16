# SDN Learning Switch Controller (POX)

## Problem Statement

Implement a controller that mimics a learning switch by dynamically learning MAC addresses and installing forwarding rules.

---

## Objective

The objective of this project is to simulate Software Defined Networking (SDN) behavior using Mininet and a POX controller. The controller learns MAC addresses dynamically, installs flow rules, and enables efficient packet forwarding.

---

## Tools Used

* Mininet
* POX Controller
* OpenFlow Protocol
* iperf (for performance testing)

---

## Project Structure

SDN_Project/
│
├── controller/
│   └── learning_switch.py
│
├── screenshots/
│   ├── controller_logs.png
│   ├── ping.png
│   ├── flows.png
│   └── iperf.png
│
└── README.md

---

## How to Run

### Step 1: Start POX Controller

cd ~/pox
python3 pox.py log.level --DEBUG openflow.of_01 SDN_Project.controller.learning_switch

---

### Step 2: Start Mininet

sudo mn --topo single,3 --controller=remote

---

### Step 3: Test Connectivity

pingall

---

### Step 4: Flow Table Inspection

sudo ovs-ofctl dump-flows s1

---

### Step 5: Performance Testing

iperf h1 h2

---

## Flow Table Analysis

The flow table in switch s1 was inspected using:
sudo ovs-ofctl dump-flows s1

Observed entries include:

* Match: Destination MAC address (dl_dst)
* Action: Output to specific port

This shows that the controller installs flow rules dynamically, allowing switches to forward packets without controller intervention after the first packet.

---

## Test Scenarios

### 1. Unknown Destination

* Packet is flooded to all ports
* Controller is involved

### 2. Known Destination

* Flow rule is installed
* Packet is forwarded directly

---

## Results

* Initial packets experience slight delay due to controller processing
* Subsequent packets are forwarded faster due to installed flow rules
* Network efficiency improves with reduced controller involvement

---

## Conclusion

The project successfully demonstrates a learning switch using SDN principles. The controller dynamically learns MAC addresses and installs flow rules, enabling efficient packet forwarding in the network.

