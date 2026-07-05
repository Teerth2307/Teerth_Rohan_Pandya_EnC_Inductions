import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    #to launch the publisher and subscriber nodes for both the custom message and the standard messages, we need to create a launch description that includes all four nodes. The launch file will start the publisher and subscriber nodes for both the custom message and the standard messages.
    
    pkg_name = 'kratos_teerth_rohan_pandya'

    return LaunchDescription([
        
        Node(package=pkg_name, executable='rover_status_publisher.py', name='rover_status_publisher_node', output='screen'
        ),
       
        Node(package=pkg_name, executable='rover_status_subscriber.py', name='rover_status_subscriber_node', output='screen'
        ),
        
        Node(package=pkg_name, executable='rover_status_msg_publisher.py', name='custom_msg_pub_node', output='screen'
        ),
       
        Node(package=pkg_name, executable='rover_status_msg_subscriber.py', name='custom_msg_sub_node', output='screen'
        )
    ])