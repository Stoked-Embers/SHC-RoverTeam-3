#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import pygame
import threading
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QMetaObject, Qt, Q_ARG
from data_relay.groundstation import Ui_MainWindow
from pygame.locals import *

from std_msgs.msg import String

class TalkerNode(Node):


    def __init__(self, ui=None):
        super().__init__("groundstation_node")
        pygame.init()
        pygame.display.init()
        screen = pygame.display.set_mode((1,1), pygame.NOFRAME)

        
        self.joystick = pygame.joystick.Joystick(0)

        self.running = True

        self.ui = ui

        self.publisher_ = self.create_publisher(String, '/pico/command', 10)

        self.listener_ = self.create_subscription(
            String, '/pico/output', self.listener_callback, 10)
        self.listener_

        self.motor_speed = 0
        self.selected_motor_speed = 0
        self.create_timer(0.5, self.timer_callback)
    
    def start_ui(self):
        self.ui_thread = threading.Thread(target=self.run_ui)
        self.ui_thread.start()
    
    def run_ui(self):
        app = QApplication(sys.argv)
        MainWindow = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow)
        MainWindow.show()
        app.exec_()

    def stop(self):
        pygame.quit()
        self.ui_thread.join()

    def update_global_speed(self):
        if self.ui and hasattr(self.ui, 'globalMotorSpeedSpinBox'):
            QMetaObject.invokeMethod(self.ui.globalMotorSpeedSpinBox, "setValue", Qt.QueuedConnection, Q_ARG(int, self.selected_motor_speed))

    def listener_callback(self, msg):
        self.get_logger().info(msg.data + "\n")

    def timer_callback(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.display.quit()
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.selected_motor_speed > 0:
                    self.selected_motor_speed -= 10
                    self.update_global_speed()
                if event.key == pygame.K_RIGHT and self.selected_motor_speed< 100:
                    self.selected_motor_speed += 10
                    self.update_global_speed()

            if event.type == pygame.JOYAXISMOTION:
                self.x_axis = self.joystick.get_axis(0)
                if self.x_axis < -0.5:
                    self.motor_speed = -(self.selected_motor_speed)
                elif self.x_axis > 0.5:
                    self.motor_speed = (self.selected_motor_speed)
                else:
                    self.motor_speed = 0

        if self.joystick.get_button(1) and self.selected_motor_speed < 100:
            self.selected_motor_speed += 10
            self.update_global_speed()
        if self.joystick.get_button(3) and self.selected_motor_speed > 0:
            self.selected_motor_speed -= 10
            self.update_global_speed()

        msg = String()
        msg.data = str(f"{self.motor_speed}")
        self.publisher_.publish(msg)
        self.get_logger().info(msg.data)

def main(args=None):
    rclpy.init(args=args)       # Initializes ROS2 communications & features
    node = TalkerNode()
    node.start_ui()
    try:
        ros_thread = threading.Thread(target=rclpy.spin, args=(node,))        # keeps the node alive
        ros_thread.start()
        ros_thread.join()
    except KeyboardInterrupt:
        node.get_logger().info("Shutting Down")
    finally:
        node.stop()
        rclpy.shutdown()

if __name__ == '__main__':
    main()