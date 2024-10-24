#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import pygame
import matplotlib

from std_msgs.msg import String

class TalkerNode(Node):


    def __init__(self):
        super().__init__("groundstation_node")
        pygame.init()

        infoObject = pygame.display.Info()
        self.screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), 
                                              pygame.RESIZABLE)
        pygame.display.set_caption("Rover Team 3 Base Station")
        self.running = True

        #Colors
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)
        self.BLUE = (0,85,255)
        self.GRAY = (168,168,168)

        def get_font(size):
            return pygame.font.Font(None, int(size))

        self.screen.fill((255,255,255))
        pygame.display.flip()

        self.publisher_ = self.create_publisher(String, 'groundstation_topic', 10)
        self.motor_speed = 0
        self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                pygame.display.quit()
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.motor_speed > 0:
                    self.motor_speed -= 5
                if event.key == pygame.K_RIGHT and self.motor_speed < 100:
                    self.motor_speed += 5

        print(self.counter)
        msg = String()
        msg.data = str(self.motor_speed)
        self.publisher_.publish(msg)
        self.get_logger().info("Publishing: " + msg.data)

def main(args=None):
    rclpy.init(args=args)       # Initializes ROS2 communications & features
    node = TalkerNode()
    rclpy.spin(node)            # keeps the node alive
    rclpy.shutdown()            # Ends ROS2 communications