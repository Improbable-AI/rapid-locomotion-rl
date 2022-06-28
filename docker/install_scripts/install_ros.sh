#!/bin/bash

set -euxo pipefail

apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

echo "deb http://packages.ros.org/ros/ubuntu `lsb_release -sc` main" > /etc/apt/sources.list.d/ros-latest.list

apt-get update

apt-get install -y  \
  ros-kinetic-ros-core=1.3.2-0* \
  git-core \
  python-argparse \
  python-wstool \
  python-vcstools \
  python-rosdep \
  python-dev \
  python-numpy \
  python-pip \
  python-setuptools \
  python-scipy \
  python-tk \
  gazebo7 \
  ros-kinetic-control-msgs \
  ros-kinetic-qt-build \
  ros-kinetic-gazebo-ros-control \
  ros-kinetic-gazebo-ros-pkgs \
  ros-kinetic-ros-control \
  ros-kinetic-control-toolbox \
  ros-kinetic-realtime-tools \
  ros-kinetic-ros-controllers \
  ros-kinetic-xacro \
  ros-kinetic-tf-conversions \
  ros-kinetic-python-orocos-kdl \
  ros-kinetic-orocos-kdl \
  ros-kinetic-kdl-parser-py \
  ros-kinetic-kdl-parser \
  ros-kinetic-moveit-simple-controller-manager \
  ros-kinetic-trac-ik \
  ros-kinetic-robot-state-publisher \
  ros-kinetic-gazebo-ros-pkgs \
  ros-kinetic-gazebo-ros-control \
  ros-kinetic-rgbd-launch \
  ros-kinetic-visp-hand2eye-calibration \
  ros-kinetic-ddynamic-reconfigure \
  software-properties-common

rm -rf /var/lib/apt/lists/*

pip install --upgrade pip==9.0.3

pip install rospkg
pip install -U catkin_tools
