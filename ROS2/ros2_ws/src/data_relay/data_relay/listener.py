#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class ListenerNode(Node):

    def __init__(self):
        super().__init__("listener_node")
        self.listener_ = self.create_subscription(
            String, 'motor_topic', self.listener_callback, 10)
        self.listener_

    def listener_callback(self, msg):
        self.get_logger().info(msg.data + "\n")


def main(args=None):
    rclpy.init(args=args)
    node = ListenerNode()
    rclpy.spin(node)
    rclpy.shutdown()