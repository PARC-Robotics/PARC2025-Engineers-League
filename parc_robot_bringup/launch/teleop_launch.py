# Launch joystick used to drive the robot

import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch_ros.actions import Node

from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    use_sim_time = LaunchConfiguration("use_sim_time")

    joy_params = os.path.join(
        get_package_share_directory("parc_robot_bringup"), "config", "joystick.yaml"
    )

    joy_node = Node(
        package="joy",
        executable="joy_node",
        parameters=[joy_params, {"use_sim_time": use_sim_time}],
    )

    teleop_node = Node(
        package="teleop_twist_joy",
        executable="teleop_node",
        name="teleop_node",
        parameters=[joy_params],
        remappings=[("/cmd_vel", "/robot_base_controller/cmd_vel_unstamped")],
    )

    twist_stamper = Node(
            package='twist_stamper',
            executable='twist_stamper',
            parameters=[{'use_sim_time': use_sim_time}],
            remappings=[('/cmd_vel_in','/robot_base_controller/cmd_vel_unstamped'),
                        ('/cmd_vel_out','/robot_base_controller/cmd_vel')]
         )
    
    return LaunchDescription([joy_node, teleop_node, twist_stamper])
