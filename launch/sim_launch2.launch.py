# launch file with added spawner scripts
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


from launch_ros.actions import Node

from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit
#import xacro


def generate_launch_description():

    # Specify the name of the package and path to xacro file within the package
    package_name = 'robot1'

    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(package_name),'launch','rsp.launch.py'
            )]), launch_arguments={'use_sim_time':'true', 'use_ros2_control': 'true'}.items()
            )

    #file_subpath = 'description/robot.urdf.xacro'


    # Use xacro to process the file
    #xacro_file = os.path.join(get_package_share_directory(pkg_name),file_subpath)
    #robot_description_raw = xacro.process_file(xacro_file).toxml()


    # Configure the node
    #node_robot_state_publisher = Node(
    #    package='robot_state_publisher',
    #    executable='robot_state_publisher',
    #    output='screen',
    #    parameters=[{'robot_description': robot_description_raw,
    #    'use_sim_time': True}] # add other parameters here if required
    #)



    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),
        )


    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                    arguments=['-topic', 'robot_description',
                                '-entity', 'my_bot'],
                    output='screen')

    #ctrl_manager = Node(
    #    package="controller_manager",
    #    executable="ros2_control_node",
    #    parameters=["robot1.urdf.xacro", "/home/rosvm/dev_ws/src/robot1/config/robot1_controllers1.yaml"]
    #)

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_ctrl"],
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_bc"],
    )

    delayed_diff_drive_spawner = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_entity,
            on_exit=[diff_drive_spawner],
        )
    )
     # Code for delaying a node (I haven't tested how effective it is)
    # 
    # First add the below lines to imports
    # from launch.actions import RegisterEventHandler
    # from launch.event_handlers import OnProcessExit
    #
    # Then add the following below the current diff_drive_spawner
    # delayed_diff_drive_spawner = RegisterEventHandler(
    #     event_handler=OnProcessExit(
    #         target_action=spawn_entity,
    #         on_exit=[diff_drive_spawner],
    #     )
    # )
    #
    # Replace the diff_drive_spawner in the final return with delayed_diff_drive_spawner



    # Run the node
    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,

        #diff_drive_spawner,
        delayed_diff_drive_spawner,
        joint_broad_spawner
    ])


