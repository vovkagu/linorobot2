# Linorobot2 Overview

This file and its sub-pages can be viewed as web pages [here](https://paulbouchier.github.io/linorobot2)

If you're planning to build your own custom ROS2 robot (2WD, 4WD, Mecanum Drive) using commonly-used parts and a microcontroller for low-level control, then the linorobot2 system may be a good fit for you. It provides these benefits:

- Microcontroller firmware runs low-level high-frequency control loops doing speed and direction control on a physical robot. Firmware built with PlatformIO.
- Micro-ros passing ROS messages between microcontroller firmware and ROS nodes including Nav2 ROS navigation software.
- Extending ROS topic subscribers and publishers out to the microcontroller makes it easy to add custom robot hardware controlled by the microcontroller. No need to modify the communication channel for new messages. Standard process for defining custom messages makes it easy to extend.
- Highly parameterized configuration files enable easy adaptation to a variety of different physical robots
- Architected extension points in linorobot2_hardware ease addition of custom devices
- ROS nodes and launch files adapt micro-ros-based firmware to Nav2 navigation nodes
- Rviz visualization of both physical and simulated robots
- Test ROS-level software in a Gazebo simulation

Linorobot2 software and firmware are contained in two repositories:
- linorobot2 (this repo): the ROS2 side of the software, including gazebo interfaces
- [linorobot2_hardware](https://github.com/linorobot/linorobot2_hardware): the microcontroller side of the firmware, including micro-ros.

This repository contains launch files to easily integrate your DIY robot
with the Nav2 navigation package, and a simulation pipeline to run and
verify your experiments on a virtual robot in Gazebo.

## Terminology

Several terms used from here on are defined below. They are names, and
are capitalized when used.

- Physical Robot: The mechanics and electronics and software
(wheels, motors sensors, onboard microcontroller and its firmware)
that has a physical presence and navigates the physical world.

- Simulated Robot: A robot instantiated in the Gazebo simulator. It has
no physical presence, and its interactions with the simulated world
it's placed in (e.g. sensing objects) are all virtual. ROS messages to/from the
simulation make the simulated robot indistinguishable to ROS nodes from
a Physical Robot.

- Microcontroller: An ESP32 or Pico microcontroller running firmware that
interacts with the sensors and actuators of a physical robot

- Workstation: A physical computer that enables the user to use ROS
commands and GUIs and interact with the Robot Computer software and
simulator, whereever they may be running. It may also reprogram
Microcontroller firmware

- Robot Computer: A computer which runs the ROS nodes which talk to the
Microcontroller of a physical robot and control it. The Robot Computer may be a
physical computer such as a Raspberry Pi on a physical robot, or
a conceptual computer running ROS nodes offboard (e.g. on the user's
Workstation).

- Simulation Computer: A computer which runs a Gazebo simulation
of a simulated robot, and the ROS nodes which drive the simulated
robot. It may be a docker instance running in the cloud, or a
conceptual computer running the simulation on the user's Workstation.

- Linorobot2 Repo: The main GitHub repo containing the launchfiles
and configurations to run the ROS nodes on a Physical or Simulated Robot.

- Linorobot2_hardware Repo: A secondary GitHub repo containing firmware
for a Physical Robot's Microcontroller, and documentation describing
how to build and configure a Physical Robot

## Configurations

Software in these repos supports two major configuration, each with two hardware
variations. These configurations and variations are important because you
use different commands and arguments to make each variation work.

### Robot Computer Configuration

The onboard Robot Computer runs the ROS nodes that control a Physical Robot, while
the Microcontroller handles encoders, motors and other hardware. Onboard serial
communication passes ROS messages between the Robot Computer and the Microcontroller.
Developer interaction with ROS happens on an external Workstation.

### Robot Wifi Configuration

The offboard Robot Computer runs the ROS nodes that control a Physical
Robot. The Microcontroller handles encoders, motors and other hardware.
Wifi passes ROS messages between the Robot Computer and the Microcontroller.
The Robot Computer and the external Workstation are one and the same, and
developer interaction with ROS happens on it.

### Workstation Simulation Configuration

The user's Workstation runs a simulation of the robot and its environment
in the Gazebo simulator, and also the ROS nodes that control the
Simulated Robot. Developer interaction with ROS happens on the Workstation
too.

### Cloud Simulation Configuration

A compute node in the cloud runs a simulation of the robot and its
environment under the Gazebo simulator, and also the ROS nodes that
control the Simulated Robot. Developer interaction with ROS comes
from the user's workstation via virtual KVM over VPN.

## Architectural Goals

The architectural goals of linorobot2 and linorobot2_hardware are to
enable ROS2 navigation, both on robot hardware and in gazebo simulation,
for a variety of differential-drive, skid-steer, and meccanum robots,
and to do this with a high degree of parameterization of robot hardware
characteristics and sensors and motor drivers. This should result in
reduced development effort for robot software and firmware. Physical Robot hardware
includes a Microcontroller running low-level high-frequency tasks in
firmware and communicating to ROS nodes on a Robot Computer and/or
Workstation using the micro-ros transport.  Micro-ros is central to the
architecture, and enables Microcontroller firmware to flexibly subscribe
and publish to ROS topics on the Robot Computer or Workstation, provide
service servers, and generally be a part of the ROS node graph. The
architecture includes extension points for users to add customizations
for their robots in such a way that they don't conflict with ongoing
maintenance and upgrades to the linorobot2 packages. This enables
upgrading linorobot2 software and firmware, hopefully with minimal
impact to the user's robot software and configurations in many cases.
Proper use of extension points also enables users to give back upgrades
to the core linorobot2 software and firmware without disrupting their
customizations.


Once the robot's URDF has been configured in the linorobot2_description
package, users can easily switch between booting up the Physical Robot
and spawning the Simulated Robot in Gazebo. The figure below shows the
major subsystems and launch files for running on real hardware and
in simulation.

![linorobot2_architecture](linorobot2_launchfiles.png)

Assuming you're using supported sensors and motor drivers, linorobot2
automatically launches the necessary hardware drivers, with the topics
being conveniently matched with the topics available in Gazebo. This
allows users to define parameters for high level applications (ie. Nav2
SlamToolbox, AMCL) that are common to both virtual and physical robots.

The figure below summarizes the topics available after launching a connection to a hardware robot by running **bringup.launch.py**. It also shows the functions assigned to the microcontroller for physical robot control.
![linorobot2_microcontroller](microcontroller_architecture.png)

An in-depth tutorial on how to configure the linorobot2 packages to run a physical robot is available in [linorobot2_hardware](https://github.com/linorobot/linorobot2_hardware).

### Help and Support
Issues can be filed in the usual way in the github repos for
linorobot2 and linorobot2_hardware. In addition,
anyone is welcome to join the [linorobot google group(https://groups.google.com/g/linorobot) and ask questions or discuss matters relevant to the project.

# Linorobot2 System Configurations

This section describes the three system configurations in which
linorobot software and firmware is supported and tested:
1. Robot Computer configuration
2. Robot Wifi configuration
3. Workstation Simulation configuration
4. Cloud Simulation configuration

Read about the [supported system configurations](SystemConfigurations.html)

Of course, it is intended that users modify the software and system
configs to meet the needs of their robot - for example, by adding
microcontrollers or ROS nodes or firmware enhancements. However,
deviations from the architecture of linorobot2 and linorobot2_hardware
should be considered carefully.

