#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from kratos_teerth_rohan_pandya_msgs.msg import RoverStatus

class CustomRoverPublisher(Node):
    def __init__(self):
        #to publish the custom message, we need to create a publisher for the custom message type
        super().__init__('rover_status_msg_publisher')
        self.pub = self.create_publisher(RoverStatus, '/custom_rover_status', 10)

        self.timer = self.create_timer(1.0, self.timer_callback)
        
        self.battery = 100.0

    def timer_callback(self):
        #to give all fields a value

        msg = RoverStatus()

        self.battery -= 0.5
        if self.battery < 0.0:
            self.battery = 0.0
        msg.battery_percentage = self.battery
        msg.velocity = 1.5
        msg.mode = "Normal"
        msg.emergency_stop = False

        if self.battery < 20.0:
            msg.mode = "Low Battery"

        if msg.battery_percentage < 5.0:
            msg.emergency_stop = True
            msg.velocity = 0.0

        self.pub.publish(msg)
        self.get_logger().info(f'Published Custom Msg | Bat: {msg.battery_percentage:.1f}%, Vel: {msg.velocity}, Mode: {msg.mode}, E-Stop: {msg.emergency_stop}')

def main(args=None):
    rclpy.init(args=args)
    node = CustomRoverPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
