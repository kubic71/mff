# Introduction
## Purpose
The purpose of this document is to list and document the Software Requirements of the Kobuki line-following robot taking part in the 2016 Robotic Day competition.

## Overview
The Robot's software is written using ROS framework and shall be running on a Kuboki Linux PC.

THe robot has the following sensors:
- Gyroscope
- Cliff sensors: left, center, right
- Wheel drop sensors: left, right
- 1D lidar sensor
- Bottom-mounted camera
- Reset Button



# Functional Requirements Specification


## Read Sensor Data Use Case
THe sensor hardware is connected to the robot microcontroller via a serial port or USB port.

Each sensor is read at a fixed rate.

The sensor data is published as a ROS message on the topic /kobuki/sensors/<sensor_name>


## The Motor control and actuation Use Case 
The speed of the robot is controlled by the motor control system.
The system is running as a ROS node.
The robot can be controlled by a ROS message on the topic /kobuki/cmd_vel

The message has the following structure:

```
std_msgs/Float64MultiArray

float64 linear_velocity
float64 angular_velocity
```

The linear velocity is in m/s and the angular velocity is in rad/s.


## The Silmultaneous localization and mapping (SLAM) Use Case

The robot estimates its odometry in the world coordinate system using the knowledge of the speed of each wheel and uses it with togeter with the Lidar sensor and the camera to more precisely localize the robot in the world and build the map at the same time.


## Prepare for the race Use Case

When the reset button is pressed, the robots resets its initial state and it prepares for start signal.

## Start Race

When the `Start` command is issued, the 


## The path planning Use Case

![](https://neobotix-docs.de/ros/_images/move_base_overview_tf.png)


