import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution
from launch_ros.actions import Node

def generate_launch_description():
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    pkg_project_gazebo = get_package_share_directory('ros_gz_example_gazebo')
    pkg_kabot_bringup = get_package_share_directory('kabot_bringup')
    pkg_kabot_description = get_package_share_directory('kabot_description')
    camera_xacro_path = os.path.join(pkg_kabot_description, 'urdf', 'yolo_vertical_camera.xacro')

    world_arg = DeclareLaunchArgument('world_sdf', default_value='kabot_training_yard.sdf')
    kabot_x_arg = DeclareLaunchArgument('kabot_x', default_value='0.0')
    kabot_y_arg = DeclareLaunchArgument('kabot_y', default_value='0.0')
    kabot_z_arg = DeclareLaunchArgument('kabot_z', default_value='0.0')
    kabot_roll_arg = DeclareLaunchArgument('kabot_roll', default_value='0.0')
    kabot_pitch_arg = DeclareLaunchArgument('kabot_pitch', default_value='0.0')
    kabot_yaw_arg = DeclareLaunchArgument('kabot_yaw', default_value='0.0')

    camera_height_arg = DeclareLaunchArgument('camera_height', default_value='1.5')
    camera_fov_arg = DeclareLaunchArgument('camera_horizontal_fov', default_value='${pi/4}')
    camera_width_arg = DeclareLaunchArgument('camera_image_width', default_value='1920')
    camera_height_res_arg = DeclareLaunchArgument('camera_image_height', default_value='1080')
    camera_framerate_arg = DeclareLaunchArgument('camera_update_rate', default_value='30.0')

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                pkg_ros_gz_sim,
                'launch',
                'gz_sim.launch.py'
            ])
        ),
        launch_arguments={
            'gz_args': PathJoinSubstitution([
                pkg_project_gazebo,
                'worlds',
                LaunchConfiguration('world_sdf')
            ])
        }.items(),
    )
    
    spawn_camera_node = Node(
        package='ros_gz_sim',
        executable='create',
        name='spawn_vertical_camera',
        output='screen',
        arguments=[
            '-string',
            Command([
                'xacro ', camera_xacro_path,
                ' camera_height:=', LaunchConfiguration('camera_height'),
                ' camera_horizontal_fov:=', LaunchConfiguration('camera_horizontal_fov')
            ])
        ]
    )
    camera_gazebo_ros_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{
            'config_file': os.path.join(pkg_kabot_bringup, 'config', 'yolo_record_ros_gz.yaml'),
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
                pkg_kabot_description,
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
        world_arg,
        kabot_x_arg,
        kabot_y_arg,
        kabot_z_arg,
        kabot_roll_arg,
        kabot_pitch_arg,
        kabot_yaw_arg,
        camera_height_arg,
        camera_fov_arg,
        camera_width_arg,
        camera_height_res_arg,
        camera_framerate_arg,
        gz_sim,
        spawn_camera_node,
        camera_gazebo_ros_bridge,
        spawn_kabot
    ])
