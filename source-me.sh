#!/bin/bash

WORKSPACE_ROOT_DIR=$(git rev-parse --show-toplevel)

if [ -z "${WORKSPACE_SETUP}" ]; then

  if [ -f "source /opt/ros/jazzy/setup.bash" ]; then
    source /opt/ros/jazzy/setup.bash
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


