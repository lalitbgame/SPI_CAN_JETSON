# Jetson-to-Jetson CAN Bus Communication

This project provides a robust, lightweight Python solution for establishing **CAN (Controller Area Network)** communication between two NVIDIA Jetson boards (e.g., Jetson Nano, Xavier NX, AGX Orin) using the native Linux `SocketCAN` driver network layer.

The repository contains a periodic **Sender** script and a blocking, event-driven **Receiver** script optimized for high reliability and low CPU utilization on ARM64 architectures.

---

## Hardware Requirements & Topology

Directly connecting the CAN pins of two Jetson boards together **will not work** and can damage the GPIO pins. CAN bus operates on differential voltages and requires specific physical layer hardware.

### Network Diagram


1. **CAN Transceivers:** Each Jetson board requires a dedicated CAN transceiver (e.g., TJA1050, SN65HVD230, or MCP2551) to convert 3.3V logic signals into differential `CAN_H` and `CAN_L` signals.
2. **Termination Resistors:** You **must** bridge a **$120\ \Omega$ resistor** across the `CAN_H` and `CAN_L` lines at both physical ends of your bus network to suppress signal reflections.
3. **Common Ground:** A shared ground (`GND`) wire must connect both transceivers to prevent floating potential errors.

### Pin Configuration (Jetson Nano / Xavier NX)
By default, the CAN pins on the 40-pin header are not enabled in the device tree. You must enable them before the OS will register a `can0` interface:

```bash
sudo /opt/nvidia/jetson-io/jetson-io.py

# Install Python CAN library
pip3 install python-can --break-system-packages

# Install Linux CAN debugging utilities
sudo apt-get update && sudo apt-get install can-utils
