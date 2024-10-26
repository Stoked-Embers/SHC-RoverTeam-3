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
        self.joint0_angle = 90
        self.joint1_angle = 90
        self.joint2_angle = 90
        self.currentServo = 0
        self.servoSpeedArray = [1,5,10,15]
        self.servoIndex = 0
        self.servoSpeed = self.servoSpeedArray[self.servoIndex]
        self.create_timer(0.1, self.timer_callback)
    
#----------------------------------------------------------------------------------------------

    def start_ui(self):
        self.ui_thread = threading.Thread(target=self.run_ui)
        self.ui_thread.start()

#----------------------------------------------------------------------------------------------
    
    def run_ui(self):
        app = QApplication(sys.argv)
        MainWindow = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow)
        MainWindow.show()
        app.exec_()

#----------------------------------------------------------------------------------------------

    def stop(self):
        pygame.quit()
        self.ui_thread.join()

#----------------------------------------------------------------------------------------------

    def update_global_speed(self):
        if self.ui and hasattr(self.ui, 'globalMotorSpeedSpinBox'):
            QMetaObject.invokeMethod(self.ui.globalMotorSpeedSpinBox, "setValue", Qt.QueuedConnection, Q_ARG(int, self.selected_motor_speed))

#----------------------------------------------------------------------------------------------

    def listener_callback(self, msg):
        self.get_logger().info(msg.data + "\n")

#----------------------------------------------------------------------------------------------

    def timer_callback(self):
        events = pygame.event.get()

        # BASE MOTOR CONTROLS
        self.x_axis = self.joystick.get_axis(0)
        if self.x_axis < -0.5:
            self.motor_speed = -(self.selected_motor_speed)
        elif self.x_axis > 0.5:
            self.motor_speed = (self.selected_motor_speed)
        else:
            self.motor_speed = 0
                
        # SERVO MOVEMENT CONTROLS
        self.y_axis = self.joystick.get_axis(4)
        if self.y_axis < -0.5 and (self.currentServo == 0) and (self.joint0_angle >= 0): 
            self.joint0_angle = min(130, self.joint0_angle + self.servoSpeed)
        elif self.y_axis > 0.5 and (self.currentServo == 0) and (self.joint0_angle >= self.servoSpeed):
            self.joint0_angle = min(130, self.joint0_angle - self.servoSpeed)
        elif self.y_axis < -0.5 and (self.currentServo == 1) and (self.joint0_angle >= 0): 
            self.joint0_angle = min(130, self.joint0_angle + self.servoSpeed)
        elif self.y_axis > 0.5 and (self.currentServo == 1) and (self.joint0_angle >= self.servoSpeed):
            self.joint0_angle = min(130, self.joint0_angle - self.servoSpeed)

        # hat_x, hat_y = self.joystick.get_hat(0)

        # SERVO SELECTION CONTROLS
        # if abs(hat_x) > 0.5:
        #     if self.joystick.get_hat(0) == (1,0) and self.currentServo == 0:
        #         self.currentServo += 1
        #         print(self.currentServo)
        #     elif self.joystick.get_hat(0) == (1,0) and self.currentServo == 1:
        #         self.currentServo -= 1
        #         print(self.currentServo)
        #     elif self.joystick.get_hat(0) == (-1,0) and self.currentServo == 0:
        #         self.currentServo += 1
        #         print(self.currentServo)
        #     elif self.joystick.get_hat(0) == (-1,0) and self.currentServo == 1:
        #         self.currentServo -= 1
        #         print(self.currentServo)

        # CHANGE MOTOR SPEED WITH KEYS ---- OUTDATED
        for event in events:
        #     if event.type == pygame.QUIT:
        #         pygame.display.quit()
        #         self.running = False
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_LEFT and self.selected_motor_speed > 0:
        #             self.selected_motor_speed -= 10
        #             self.update_global_speed()
        #         if event.key == pygame.K_RIGHT and self.selected_motor_speed< 100:
        #             self.selected_motor_speed += 10
        #             self.update_global_speed()

            #if event.type == pygame.JOYAXISMOTION:
                

            if event.type == pygame.JOYBUTTONDOWN:
                if self.joystick.get_button(1) and self.selected_motor_speed < 100:
                    self.selected_motor_speed += 10
                    self.update_global_speed()
                if self.joystick.get_button(3) and self.selected_motor_speed > 0:
                    self.selected_motor_speed -= 10
                    self.update_global_speed()
            
            hat_x, hat_y = self.joystick.get_hat(0)
            if abs(hat_x) > 0.5:
                if self.joystick.get_hat(0) == (1,0) and self.currentServo == 0:
                    self.currentServo += 1
                    print(self.currentServo)
                elif self.joystick.get_hat(0) == (1,0) and self.currentServo == 1:
                    self.currentServo -= 1
                    print(self.currentServo)
                elif self.joystick.get_hat(0) == (-1,0) and self.currentServo == 0:
                    self.currentServo += 1
                    print(self.currentServo)
                elif self.joystick.get_hat(0) == (-1,0) and self.currentServo == 1:
                    self.currentServo -= 1
                    print(self.currentServo)
            if abs(hat_y) > 0.5:
                if self.joystick.get_hat(0) == (0,1) and self.servoIndex < 3:
                    self.servoIndex += 1
                    self.servoSpeed = self.servoSpeedArray[self.servoIndex]
                    print(self.servoSpeed)
                elif self.joystick.get_hat(0) == (0,-1) and self.servoIndex > 0:
                    self.servoIndex -= 1
                    self.servoSpeed = self.servoSpeedArray[self.servoIndex]
                    print(self.servoSpeed)

        

        msg = String()
        msg.data = str(f"base:{self.motor_speed},ser0:{self.joint0_angle},ser1:{self.joint1_angle},ser2:{self.joint2_angle}")
        self.publisher_.publish(msg)
        self.get_logger().info(msg.data)

        pygame.event.clear()

#----------------------------------------------------------------------------------------------

def main(args=None):
    rclpy.init(args=args)       # Initializes ROS2 communications & features
    node = TalkerNode()
    node.start_ui()
    rclpy.spin(node)
    node.stop()
    rclpy.shutdown()
    #try:
    #    ros_thread = threading.Thread(target=rclpy.spin, args=(node,))        # keeps the node alive
    #    ros_thread.start()
     #   ros_thread.join()
    #except KeyboardInterrupt:
     #   node.get_logger().info("Shutting Down")
    #finally:
    #    node.stop()
     #   rclpy.shutdown()

if __name__ == '__main__':
    main()