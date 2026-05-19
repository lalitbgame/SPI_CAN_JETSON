import os
import time
import can

# 1. Bring up the CAN interface (Done once at startup)
os.system('sudo ip link set can0 down 2>/dev/null')
os.system('sudo ip link set can0 type can bitrate 500000')
os.system('sudo ip link set can0 up')

print("CAN interface initialized. Starting periodic sender...")

try:
    # 2. Initialize the bus using the native socketcan driver
    can0 = can.interface.Bus(channel='can0', interface='socketcan')
    
    # 3. Infinite loop to send data periodically
    while True:
        # Create the message payload
        msg = can.Message(
            arbitration_id=0x123, 
            data=[0, 1, 2, 3, 4, 5, 6, 7], 
            is_extended_id=False
        )
        
        try:
            can0.send(msg)
            print(f"[{time.strftime('%X')}] Message sent successfully!")
        except can.CanError:
            print(f"[{time.strftime('%X')}] Message failed to transmit.")
        
        # 4. Wait for 60 seconds before sending again
        time.sleep(60)

except KeyboardInterrupt:
    print("\nStopping sender script...")
except Exception as e:
    print(f"An error occurred: {e}")