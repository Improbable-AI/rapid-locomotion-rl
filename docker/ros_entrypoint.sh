#!/bin/bash
set -e

# setup ros environment
source "/root/catkin_ws/devel/setup.bash"

# Setting environment variable for ROS
# ROS_IP=$(ip addr show eth0 | grep -Po 'inet \K[\d.]+')
# export ROS_IP=$ROS_IP

eval "bash"

# TODO: A exit sequence for identifying failed initialization or broken Gazebo
exec "$@"
