import os
import time
import can

print("Initializing CAN interface...")

# 1. Bring up the CAN interface safely
# We temporarily bring it down, configure it, and bring it back up to avoid "Device or resource busy"
os.system('sudo ip link set can0 down 2>/dev/null')
os.system('sudo ip link set can0 type can bitrate 500000')
os.system('sudo ip link set can0 up')

print("CAN interface initialized.")
print("Receiver is active and permanently listening for data... (Press Ctrl+C to exit)\n")

try:
    # 2. Fixed Deprecation Warning: Changed 'bustype' to 'interface'
    can0 = can.interface.Bus(channel='can0', interface='socketcan')
    
    # 3. Infinite loop to constantly look for data
    while True:
        # Blocks indefinitely until a message physically arrives
        msg = can0.recv(timeout=None)
        
        if msg is not None:
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{current_time}] Data Received!")
            print(f"  ID:   {hex(msg.arbitration_id)}")
            print(f"  DLC:  {msg.dlc} bytes")
            print(f"  Data: {list(msg.data)}")
            print("-" * 40)

except KeyboardInterrupt:
    print("\nStopping receiver script...")
except Exception as e:
    print(f"An error occurred: {e}")