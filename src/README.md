For ROS2 questions

Approach:
I created publishers and subscribers for each datatype and then created a custom message definition and used python launch script to coordinate
all of the nodes together

Assumptions:
All the values for data were assumed
The custom message package is correctly configured with the necessary dependencies

Challenges:
Using the environment and docker
The docker sometimes didn't show port so couldn't access localhost on web and hence had to use a few turnabouts
Working with new python library and how it works(had to use AI to understand it)

Testing Implementation:
Used ros2 node list and ros2 topic list to confirm all nodes and topics were active
ros2 topic type /battery_level and ros2 topic echo /battery_level to verify message contents
Used ros2 interface show to ensure the custom RoverStatus message fields were correctly defined

Known limitations:
No input taken from hardware
No implementation for any kind of error like connection timeout



For IKFK questions


For Problem 1:

Approach:
Used mathematical identities i learned online

Assumptions:
Same as when they derived the expression(I couldn't find any assumptions made so I am not sure)

Challenges:
Doing the complex calculations

Testing Implementations:
Used AI to check if solution was correct

Known Limitations:
I couldn't find any


For Problem 2:

Approach:
I first maintain a position, then take input and check if the position is reachable, if it is then calculate angle using inverse kinematics and 
move the arm, else return the starting position

Assumptions:
The wrist_output_shaft_link acts as the end-effector
Z height remains Constant
URDF provided names

Challenges:
Finding dimensions
How to relay to the arm UI
Starting the arm UI in docker
Testing was hard
Had to use AI at various steps to understand

Testing Implementations:
Inputting a displacement that pushes the arm to $3.6\,\text{m}$ to verify the error message and command rejection
Running ros2 run tf2_tools view_frames to ensure the link hierarchy matches the mathematical model

Known Limitations:
Works only in XY-plane

