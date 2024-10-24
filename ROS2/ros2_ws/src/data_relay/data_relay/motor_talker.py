#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import pygame

from std_msgs.msg import String

class TalkerNode(Node):


    def __init__(self):
        super().__init__("motor_talker_node")
        pygame.init()

        screen = pygame.display.set_mode((1,1))
        running = True

        self.publisher_ = self.create_publisher(String, 'motor_topic', 10)
        self.motor_speed = 0
        self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.motor_speed -= 5
                if event.key == pygame.K_RIGHT:
                    self.motor_speed += 5

        msg = String()
        msg.data = str(self.motor_speed)
        self.publisher_.publish(msg)
        self.get_logger().info("Publishing: " + msg.data)

def main(args=None):
    rclpy.init(args=args)       # Initializes ROS2 communications & features
    node = TalkerNode()
    rclpy.spin(node)            # keeps the node alive
    rclpy.shutdown()            # Ends ROS2 communications