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
        self.ser = serial.Serial('/dev/ttyACM0', 9600)
        # Create a publisher to publish any output the pico sends
        #self.publisher = self.create_publisher(String, '/pico/output', 10) 

        # Create a subscriber to listen to any commands sent for the pico
        self.subscription = self.create_subscription(String, '/pico/command', self.send, 10)

        

    
        

    
    
    def send(self, msg):
        self.get_logger().info('recieved input: "%"' % msg.data)

        # Send command to pico
        self.ser.write(bytes(command, "utf8"))
        #print(f"[Sys] Relaying: {command}")

    
        

def main(args=None):
    rclpy.init(args=args)
    serial_publisher = SerialRelay()
    rclpy.spin(serial_publisher)
    serial_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()