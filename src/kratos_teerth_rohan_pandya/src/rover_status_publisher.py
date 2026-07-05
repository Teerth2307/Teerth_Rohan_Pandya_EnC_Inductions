#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String, Bool

class RoverStatusPublisher(Node):
    def __init__(self):
        #publishers for battery level, mode, and emergency stop status
        super().__init__('rover_status_publisher')
        
        self.battery_pub = self.create_publisher(Float32, '/battery_level', 10)
        self.mode_pub = self.create_publisher(String, '/rover_mode', 10)
        self.emergency_pub = self.create_publisher(Bool, '/emergency_stop', 10)

        self.timer = self.create_timer(1.0, self.timer_callback)

        self.battery_level = 100.0


    def timer_callback(self):
        #create messages for battery level, mode, and emergency stop status
        msg_battery = Float32()
        msg_mode = String()
        msg_estop = Bool()

        self.battery_level -= 0.5
        if self.battery_level < 0.0:
            self.battery_level = 0.0
        msg_battery.data = self.battery_level

        if self.battery_level > 20.0:
            msg_mode.data = "Normal"
        else:
            msg_mode.data = "Low Battery"

        # Fixed variable name here
        if self.battery_level <= 5.0:
            msg_estop.data = True
        else:
            msg_estop.data = False

        self.battery_pub.publish(msg_battery)
        self.mode_pub.publish(msg_mode)
        self.emergency_pub.publish(msg_estop)

        self.get_logger().info(f'Publishing: Battery={msg_battery.data:.1f}%, Mode={msg_mode.data}, Emergency-Stop={msg_estop.data}')


def main(args=None):
    rclpy.init(args=args)
    node = RoverStatusPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
