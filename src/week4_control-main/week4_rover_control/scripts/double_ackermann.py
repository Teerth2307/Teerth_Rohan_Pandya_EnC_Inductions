#!/usr/bin/env python3
import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64MultiArray

class DoubleAckermannController(Node):
    def __init__(self):
        super().__init__('double_ackermann_controller')
        
        # Subscribe to teleop/joystick commands
        self.cmd_sub = self.create_subscription(
            Twist, 
            '/cmd_vel', 
            self.cmd_callback, 
            10
        )
        
        # Publisher for the 4 steering hinges (Position in Radians)
        # Order matches YAML: [fl_steer, fr_steer, rl_steer, rr_steer]
        self.steer_pub = self.create_publisher(
            Float64MultiArray, 
            '/steering_controller/commands', 
            10
        )

        # Publisher for the 4 wheel axles (Velocity in Rad/s)
        # Order matches YAML: [fl_drive, fr_drive, rl_drive, rr_drive]
        self.drive_pub = self.create_publisher(
            Float64MultiArray, 
            '/drive_controller/commands', 
            10
        )

        # Rover Physical Constants
        self.wheelbase = 0.4 
        self.track_width = 0.6
        self.wheel_radius = 0.12

        self.get_logger().info("Double Ackermann Controller Node Started. Waiting for /cmd_vel...")
        
    def calculate_wheel_kinematics(self, v_linear, omega, x, y):
        
        #Calculates the required steering angle and drive velocity for one wheel.
        
        # Calculate velocity components at this wheel's coordinates
        v_wheel_linear = v_linear - (omega * y)
        v_wheel_angular = omega * x

        # Calculate the magnitude and direction 
        speed = math.hypot(v_wheel_linear, v_wheel_angular)
        steering_angle = math.atan2(v_wheel_angular, v_wheel_linear)

        # Enforce the steering limits
        if steering_angle > math.pi / 2.0:
            steering_angle -= math.pi
            speed = -speed
        elif steering_angle < -math.pi / 2.0:
            steering_angle += math.pi
            speed = -speed

        # Convert the linear speed to wheel angular velocity for motors
        wheel_angular_vel = speed / self.wheel_radius

        return steering_angle, wheel_angular_vel

    def cmd_callback(self, msg):
        linear_x = msg.linear.x
        angular_z = msg.angular.z
        
        # =======================================================
        # APPLICANT TASK: Implement Double Ackermann Kinematics 
        # Calculate the 4 steering angles and 4 wheel velocities
        # =======================================================
        # Front-Left (FL):  +X, +Y
        fl_angle, fl_vel = self.calculate_wheel_kinematics(linear_x, angular_z, self.wheelbase / 2, self.track_width / 2)
        
        # Front-Right (FR): +X, -Y
        fr_angle, fr_vel = self.calculate_wheel_kinematics(linear_x, angular_z, self.wheelbase / 2, -self.track_width / 2)
        
        # Rear-Left (RL): -X, +Y
        rl_angle, rl_vel = self.calculate_wheel_kinematics(linear_x, angular_z, -self.wheelbase / 2, self.track_width / 2)
        
        # Rear-Right (RR): -X, -Y
        rr_angle, rr_vel = self.calculate_wheel_kinematics(linear_x, angular_z, -self.wheelbase / 2, -self.track_width / 2)
        # 1. Calculate angles (radians)
        #fl_angle, fr_angle, rl_angle, rr_angle = 0.0, 0.0, 0.0, 0.0
        
        # 2. Calculate velocities (rad/s)
        #fl_vel, fr_vel, rl_vel, rr_vel = 0.0, 0.0, 0.0, 0.0
        
        # =======================================================
        
        # Publish Steering Commands
        steer_msg = Float64MultiArray()
        steer_msg.data = [fl_angle, fr_angle, rl_angle, rr_angle]
        self.steer_pub.publish(steer_msg)

        # Publish Drive Commands
        drive_msg = Float64MultiArray()
        drive_msg.data = [fl_vel, fr_vel, rl_vel, rr_vel]
        self.drive_pub.publish(drive_msg)

def main(args=None):
    rclpy.init(args=args)
    node = DoubleAckermannController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
