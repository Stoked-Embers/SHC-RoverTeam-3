import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/wyatt/Documents/GitHub/SHC-RoverTeam-3/ROS2/ros2_ws/install/pico_relay'
