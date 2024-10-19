#do source /opt/ros/humble/setup.bash in the terminal (doing this in the ROS2 directory worked for me - wyatt)
import rclpy
from rclpy.node import Node

from std_msgs.msg import String 

class publisher(Node):
    def __init__(self):
        super().__init__('publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timeBetweenMessages = 1.0; # 1 second between messages
        self.timer = self.create_timer(timeBetweenMessages, self.timer_trigger)
        self.triggerCount = 0 # this establishes a counter to use for when the timer is triggered

    def timer_trigger(self):
        message = String()
        message.data = 'This is a test of the ROS2 Publisher' % self.triggerCount
        self.publisher_publish(message)
        self.get_logger().info('Publishing:' % message.data)
        self.triggerCount +=1

def main(args = None):
    rclpy.init(args= args) #TODO: What args do we need?
    publisher = publisher() #! TODO: This seems weird
    rclpy.spin(publisher)

    publisher.destroy_node()
    rclpy.shtudown()

if __name__ == '__main__':
    main()



