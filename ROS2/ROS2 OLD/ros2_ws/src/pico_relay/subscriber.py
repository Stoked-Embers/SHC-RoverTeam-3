# Most of this is similar to the publisher code

import rclpy
from rclpy.node import Node

from std_msgs.msg import String 

class publisher(Node):
    def __init__(self):
        super().__init__('publisher')
        self.subscription= self.create_subscription(String, topic, self.printMessage)
        self.subscription

    def printMessage(self):
        self.get_logger().info('Message:' % msg.data) 



def main(args = None):
    rclpy.init(args= args) #TODO: What args do we need?
    publisher = publisher() 
    rclpy.spin(publisher)

    publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()



