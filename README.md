# MindCloud_ERC22_Nav

## Installation

Clone the packages directly into your src folder in your catkin workspace.
Make sure you installed RTABMap binaries, use the following link for guidance [here](https://github.com/introlab/rtabmap_ros).

## Installing dependencies
```
$ sudo apt-get install ros-noetic-tf2-sensor-msgs
$ sudo apt-get install ros-noetic-tf2-tools ros-noetic-tf
```
And just to be safe, run the following.
```
$ rosdep install --rosdistro noetic --from-paths src -iy
```

## Fake Frame approach

Runs the approach of flattening base_link -> map tf into a fake frame and filtering the point cloud, code is thoroughly commented in the leo_navigation
package source folder.

## To run

Either test with your real-life Leo Rover or with a simulation provided [here](https://github.com/EuropeanRoverChallenge/ERC-Remote-Navigation-Sim).

Launches the RTAB-Map
```
roslaunch launch_packages mapping.launch
```
Launches the flattener + filter + move_base
```
roslaunch launch_packages navigation.launch
