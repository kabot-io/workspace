import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution

from launch_ros.actions import Node

def generate_launch_description():
    kabot_bringup_pkg_dir = get_package_share_directory('kabot_bringup')
    kabot_description_pkg_dir = get_package_share_directory('kabot_description')
    pkg_project_gazebo = get_package_share_directory('ros_gz_example_gazebo')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': PathJoinSubstitution([
            pkg_project_gazebo,
            'worlds',
            'kabot_training_yard.sdf'
        ])}.items(),
    )

    sdf_file  =  os.path.join(kabot_description_pkg_dir, 'models', 'kabot', 'model.sdf')
    with open(sdf_file, 'r') as infp:
        robot_desc = infp.read()

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='both',
        parameters=[
            {'use_sim_time': True},
            {'robot_description': robot_desc},
        ]
    )

    rviz = Node(
       package='rviz2',
       executable='rviz2',
       arguments=['-d', os.path.join(kabot_bringup_pkg_dir, 'config', 'diff_drive.rviz')],
       condition=IfCondition(LaunchConfiguration('rviz'))
    )
    rviz_arg = DeclareLaunchArgument('rviz', default_value='false', description='Open RViz.')

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{
            'config_file': os.path.join(kabot_bringup_pkg_dir, 'config', 'ros_gz_example_bridge.yaml'),
            'qos_overrides./tf_static.publisher.durability': 'transient_local',
        }],
        output='screen'
    )

    spawn_kabot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                get_package_share_directory('ros_gz_sim'),
                'launch',
                'gz_spawn_model.launch.py'
            ])
        ),
        launch_arguments={
            'world': 'kabot_training_yard',
            'file': PathJoinSubstitution([
                kabot_description_pkg_dir,
                'models/kabot',
                'model.sdf'
            ]),
            'name': 'kabot_robot',
            'x': '0.0',
            'y': '0.0',
            'z': '0.0'
        }.items(),
    )

    return LaunchDescription([
        gz_sim,
        spawn_kabot,
        rviz_arg,
        bridge,
        robot_state_publisher,
        rviz
    ])
