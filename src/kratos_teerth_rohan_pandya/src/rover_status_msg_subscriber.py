#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from kratos_teerth_rohan_pandya_msgs.msg import RoverStatus

class CustomRoverSubscriber(Node):
    def __init__(self):
        #subscribe to the custom message topic
        super().__init__('rover_status_msg_subscriber')
        self.sub = self.create_subscription( RoverStatus, '/custom_rover_status', self.listener_callback, 10)

    def listener_callback(self, msg): 
        #log the received message fields
        self.get_logger().info(f'Battery   : {msg.battery_percentage:.1f}%')
        self.get_logger().info(f'Velocity  : {msg.velocity} m/s')
        self.get_logger().info(f'Mode      : {msg.mode}')
        self.get_logger().info(f'E-Stop    : {msg.emergency_stop}')
    

def main(args=None):
    rclpy.init(args=args)
    node = CustomRoverSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()