# Getting Started

## 1. Install WSL2 Ubuntu 24.04 + Gazebo Harmonic
Source: https://aleksandarhaber.com/how-to-install-gazebo-harmonic-in-windows-by-using-wsl-and-ubuntu-24-04-and-how-to-run-mobile-robot-simulation/

## 2. Clone this repo
``` 
git clone git@github.com:kabot-io/workspace.git
```

## 3. Install ROS 2 Jazzy 
Source: https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html


## 4. Setup your workspace
``` 
source ~/workspace/source-me.sh
```

build eveyrthing and compile commands, also run
```bash
colcon build --event-handlers console_direct+ --cmake-args -DCMAKE_EXPORT_COMPILE_COMMANDS=ON && source install/setup.zsh && ros2 launch kabot_bringup simple.launch.py
```


## 5. Install dependencies:

```bash
rosdep install --from-paths src --ignore-src --os ubuntu:noble  -r -i -y --rosdistro jazzy
```

## 5. PRACUJ DZIELNIE
