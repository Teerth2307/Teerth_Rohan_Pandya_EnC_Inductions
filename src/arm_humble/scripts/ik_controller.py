#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math
import threading
import sys  

class ArmIKController(Node):
    def __init__(self):
        super().__init__('ik_controller')
        
        self.joint_pub = self.create_publisher(JointState, '/joint_states', 10)
        self.timer = self.create_timer(0.1, self.publish_joint_states)
        
        # Exact dimensions extracted from urdf/my_custom_arm.urdf.xacro
        self.L1 = 0.35      # Length from shoulder to elbow
        self.L2 = 0.42      # Length from elbow to wrist_output_shaft
        self.Z_BASE = 0.17  # Z-axis offset from ground to shoulder_joint

        # Initial end effector position (x, y, z)
        self.current_x = self.L1 + self.L2
        self.current_y = 0.0
        self.current_z = self.Z_BASE
        
        # Current joint states
        self.yaw_angle = 0.0
        self.shoulder_angle = 0.0
        self.elbow_angle = 0.0

        # Compute initial angles
        self.update_joints_from_ik(self.current_x, self.current_y, self.current_z)

        # Launch the terminal input loop in a separate thread so it does not block ROS spin(AI asked me to do this to make code better)
        self.input_thread = threading.Thread(target=self.user_input_loop)
        self.input_thread.daemon = True
        self.input_thread.start()

    def compute_ik(self, x, y, z):
        """
        Calculates Inverse Kinematics for the 3-DOF arm.
        Returns a tuple (yaw, shoulder, elbow) if reachable, or None if not.
        """
        # 1. Calculate Base Yaw
        yaw_calc = math.atan2(y, x)

        # 2. Calculate planar distance from shoulder joint
        r = math.sqrt(x**2 + y**2)
        z_eff = z - self.Z_BASE 
        d = math.sqrt(r**2 + z_eff**2)

        # Reachability check
        if d > (self.L1 + self.L2) or d < abs(self.L1 - self.L2):
            return None # Target is outside reach

        # 3. Calculate Elbow Angle (Law of Cosines)
        cos_elbow = (r**2 + z_eff**2 - self.L1**2 - self.L2**2) / (2 * self.L1 * self.L2)
        cos_elbow = max(min(cos_elbow, 1.0), -1.0) # To avoid domain errors due to floating point inaccuracies
        
        # Elbow down configuration
        elbow_calc = math.acos(cos_elbow) 

        # 4. Calculate Shoulder Angle
        alpha = math.atan2(z_eff, r)
        beta = math.atan2(self.L2 * math.sin(elbow_calc), self.L1 + self.L2 * math.cos(elbow_calc))
        
        shoulder_calc = alpha - beta 

        return (yaw_calc, shoulder_calc, elbow_calc)

    def update_joints_from_ik(self, x, y, z):
        """Attempts to update joint angles and publish if target is valid."""
        joints = self.compute_ik(x, y, z)
        
        if joints is None:
            self.get_logger().error(f"\nTarget position ({x:.2f}, {y:.2f}, {z:.2f}) is unreachable! Command rejected.")
            return False
            
        self.yaw_angle, self.shoulder_angle, self.elbow_angle = joints
        self.current_x, self.current_y, self.current_z = x, y, z
        self.publish_joint_states()
        return True

    def publish_joint_states(self):
        """Constructs and publishes the JointState message."""
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        
        # Names mapped exactly to your joint_state_publisher
        msg.name = ['base_yaw_joint', 'shoulder_joint', 'elbow_joint', 'wrist_pitch_joint', 'wrist_roll_joint', 'gripper_joint']
        msg.position = [self.yaw_angle, self.shoulder_angle, self.elbow_angle, 0.0, 0.0, 0.0]
        
        self.joint_pub.publish(msg)

    def user_input_loop(self):
        """Handles terminal prompts and target updates."""
        while rclpy.ok():
            print(f"\nCurrent End Effector Position:\nx = {self.current_x:.2f}\ny = {self.current_y:.2f}\nz = {self.current_z:.2f}")
            
            axis = input("Enter axis to move (x/y/z): ").strip().lower()
            if axis not in ['x', 'y', 'z']:
                print("Invalid axis. Please enter x, y, or z.")
                continue
                    
            disp_str = input("Enter displacement (meters): ").strip()
            displacement = float(disp_str)
                
                # Propose new target
            target_x = self.current_x + displacement if axis == 'x' else self.current_x
            target_y = self.current_y + displacement if axis == 'y' else self.current_y
            target_z = self.current_z + displacement if axis == 'z' else self.current_z
                
            print(f"The new target position becomes:\nx = {target_x:.2f}\ny = {target_y:.2f}\nz = {target_z:.2f}")
                
                # Attempt to move
            success = self.update_joints_from_ik(target_x, target_y, target_z)
            if not success:
                print("Preserving previous robot configuration.")
                

def main(args=None):
    rclpy.init(args=args)
    node = ArmIKController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
