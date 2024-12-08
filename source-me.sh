#!/bin/bash

WORKSPACE_ROOT_DIR=$(git rev-parse --show-toplevel)

if [ -z "${WORKSPACE_SETUP}" ]; then

  if [ -f "/opt/ros/jazzy/setup.bash" ]; then
    source /opt/ros/jazzy/setup.bash
    source $WORKSPACE_ROOT_DIR/install/setup.bash
  else
    echo "setup.bash not found. Please, install ROS2 Jazzy"
  fi

  # Colors
  COLOR_RED='\033[0;31m'
  COLOR_GREEN='\033[0;32m'
  COLOR_BLUE='\033[0;34m'
  COLOR_YELLOW='\033[1;33m'
  NO_COLOR='\033[0m'

  export WORKSPACE_SETUP=1
fi

kabot-rebuild(){
    cd $WORKSPACE_ROOT_DIR
    rm -rf build log install
    colcon build
    source install/setup.bash
}

kill-gazebo(){
  pkill -f gzserver
  pkill -f gzclient
}

kabot-sdf(){
    xacro_file="$WORKSPACE_ROOT_DIR/src/kabot_description/urdf/kabot.xacro"
    urdf_file="${xacro_file%.xacro}.urdf"
    sdf_file="$$WORKSPACE_ROOT_DIR/src/kabot_description/models/kabot/kabot.sdf"
    ros2 run xacro xacro $xacro_file -o $urdf_file
    gz sdf -p $urdf_file > $sdf_file
    echo "Converted $xacro_file to $sdf_file"
}
