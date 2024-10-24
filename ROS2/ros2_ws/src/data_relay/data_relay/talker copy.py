#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class TalkerNode(Node):

    def __init__(self):
        super().__init__("talker_node")
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        self.counter_ = 0
        self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        msg = String()
        msg.data = "Test message " + str(self.counter_)
        self.publisher_.publish(msg)
        self.get_logger().info("Publishing: " + msg.data)
        self.counter_ +=1

def main(args=None):
    rclpy.init(args=args)       # Initializes ROS2 communications & features
    node = TalkerNode()
    rclpy.spin(node)            # keeps the node alive
    rclpy.shutdown()            # Ends ROS2 communications