import rclpy
from rclpy.node import Node

import serial
import sys
import threading
import glob

from std_msgs.msg import String

class SerialRelay(Node):
    def __init__(self):
        # Initalize node with name
        super().__init__("serial_publisher")

        # Create a publisher to publish any output the pico sends
        
        self.ser = serial.Serial('/dev/ttyACM0', 9600)
        # Create a publisher to publish any output the pico sends
        #self.publisher = self.create_publisher(String, '/pico/output', 10) 

        # Create a subscriber to listen to any commands sent for the pico
        self.publisher = self.create_publisher(String, '/pico/output', 10) 
        self.create_timer(0.1, self.read_pico)
    
    
    def run(self):
        # This thread makes all the update processes run in the background
        thread = threading.Thread(target=rclpy.spin, args={self}, daemon=True)
        thread.start()
        
        try:
            while rclpy.ok():
                # Check the pico for updates
                self.read_pico()

        except KeyboardInterrupt:
            sys.exit(0)

    def read_pico(self):
        output = str(self.ser.readline(), "utf8")
        # If received output
        if output:
        
            # Create a string message object
            msg = String()

            
            self.posXYZ, self.acceleration, self.atmospheric = output.split("$")
            self.get_logger().info(f"{self.posXYZ} {self.acceleration} {self.atmospheric}")
            # Publish data
            self.publisher.publish(msg)
            #print(f"[Pico] Publishing: {msg}")
        

def main(args=None):
    rclpy.init(args=args)
    serial_publisher = SerialRelay()
    rclpy.spin(serial_publisher)
    serial_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
