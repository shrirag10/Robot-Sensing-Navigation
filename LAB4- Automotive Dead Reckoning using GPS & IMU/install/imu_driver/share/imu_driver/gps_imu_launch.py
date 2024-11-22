from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument

def generate_launch_description():
    return LaunchDescription([
        # GPS Port Configuration
        DeclareLaunchArgument(
            'gps_port',
            default_value='/dev/ttyUSB0',
            description='Serial port for GPS puck'
        ),
        
        # IMU Port Configuration
        DeclareLaunchArgument(
            'imu_port',
            default_value='/dev/ttyUSB1',
            description='Serial port for IMU'
        ),
        
        # GPS Driver Node
        Node(
            package='gps_driver',
            executable='driver',  # Adjust this to match the actual executable name
            name='gps_driver',
            output='screen',
            parameters=[{'port': LaunchConfiguration('gps_port')}]
        ),
        
        # IMU Driver Node
        Node(
            package='imu_driver',
            executable='imu',  # Adjust this to match the actual executable name
            name='IMU',
            output='screen',
            emulate_tty=True,
            parameters=[
                {'port': LaunchConfiguration('imu_port')},
                {'baudrate': 115200},
                {'sampling_rate': 40.0}
            ],
            arguments=['--ros-args', '--log-level', 'debug']
        ),
    ])

