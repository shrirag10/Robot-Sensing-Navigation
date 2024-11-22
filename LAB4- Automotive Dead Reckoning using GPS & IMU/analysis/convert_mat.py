import os
import numpy as np
#import rosbag2_py
from rclpy.serialization import deserialize_message
#from sensor_msgs.msg import Imu
#from gps_msgs.msg import GPSmsg
from scipy.io import savemat
from pathlib import Path
from rosbags.highlevel import AnyReader
from rosbags.typesys import Stores, get_typestore, get_types_from_msg

def find_db_file(bag_folder):
    for file in os.listdir(bag_folder):
        if file.endswith('.db3'):
            return os.path.join(bag_folder, file)
    raise FileNotFoundError(f"No .db3 file found in {bag_folder}")

def read_sensor_data_from_bag(bag_folder, imu_topic, gps_topic):
    # Use AnyReader for flexibility
    bagpath = Path(bag_folder)
    typestore = get_typestore(Stores.ROS2_HUMBLE)
    add_types = {}
    add_types.update(get_types_from_msg(imu_topic, 'imu_msgs/msg/IMUmsg'))
    add_types.update(get_types_from_msg(gps_topic, 'gps_msgs/msg/GPSmsg'))
    typestore.register(add_types)
    imu_data = []
    gps_data = []
    
    with AnyReader([bagpath], default_typestore=typestore) as reader:
    	imu_connections = [x for x in reader.connections if x.topic == '/imu']
    	gps_connections = [y for y in reader.connections if y.topic == '/gps']
    	# Process IMU data
    	for connection, timestamp, data in reader.messages(connections=imu_connections):
            imu_msg = reader.deserialize(data, connection.msgtype)
            imu_data.append({
                'timestamp': imu_msg.header.stamp.sec + imu_msg.header.stamp.nanosec * 1e-9,  # Convert to seconds
                'angular_velocity_x': imu_msg.imu.angular_velocity.x,
                'angular_velocity_y': imu_msg.imu.angular_velocity.y,
                'angular_velocity_z': imu_msg.imu.angular_velocity.z,
                'linear_acceleration_x': imu_msg.imu.linear_acceleration.x,
                'linear_acceleration_y': imu_msg.imu.linear_acceleration.y,
                'linear_acceleration_z': imu_msg.imu.linear_acceleration.z,
                'orientation_x': imu_msg.imu.orientation.x,
                'orientation_y': imu_msg.imu.orientation.y,
                'orientation_z': imu_msg.imu.orientation.z,
                'orientation_w': imu_msg.imu.orientation.w,
                'angular_velocity_covariance': imu_msg.imu.angular_velocity_covariance,
                'linear_acceleration_covariance': imu_msg.imu.linear_acceleration_covariance,
                'orientation_covariance': imu_msg.imu.orientation_covariance,
                'magnetometer_x':imu_msg.mag_field.magnetic_field.x,
                'magnetometer_y':imu_msg.mag_field.magnetic_field.y,
                'magnetometer_z':imu_msg.mag_field.magnetic_field.z
            })
        # Process GPS data
    	for connection, timestamp, data in reader.messages(connections=gps_connections):
            gps_msg = reader.deserialize(data, connection.msgtype)
            gps_data.append({
                'timestamp': gps_msg.header.stamp.sec + gps_msg.header.stamp.nanosec * 1e-9,  # Convert to seconds
                'latitude': gps_msg.latitude,
                'longitude': gps_msg.longitude,
                'altitude': gps_msg.altitude,
                'utm_easting': gps_msg.utm_easting,
                'utm_northing': gps_msg.utm_northing,
                'zone': gps_msg.zone,
                'letter': gps_msg.letter
            })
    
    return imu_data, gps_data

def convert_to_mat(imu_data, gps_data, mat_file_path):
    # Prepare data for saving into a .mat file
    data = {
        'imu': {
            'timestamps': np.array([msg['timestamp'] for msg in imu_data]),
            'angular_velocity_x': np.array([msg['angular_velocity_x'] for msg in imu_data]),
            'angular_velocity_y': np.array([msg['angular_velocity_y'] for msg in imu_data]),
            'angular_velocity_z': np.array([msg['angular_velocity_z'] for msg in imu_data]),
            'linear_acceleration_x': np.array([msg['linear_acceleration_x'] for msg in imu_data]),
            'linear_acceleration_y': np.array([msg['linear_acceleration_y'] for msg in imu_data]),
            'linear_acceleration_z': np.array([msg['linear_acceleration_z'] for msg in imu_data]),
            'orientation_x': np.array([msg['orientation_x'] for msg in imu_data]),
            'orientation_y': np.array([msg['orientation_y'] for msg in imu_data]),
            'orientation_z': np.array([msg['orientation_z'] for msg in imu_data]),
            'orientation_w': np.array([msg['orientation_w'] for msg in imu_data]),
            'angular_velocity_covariance': np.array([msg['angular_velocity_covariance'] for msg in imu_data]),
            'linear_acceleration_covariance': np.array([msg['linear_acceleration_covariance'] for msg in imu_data]),
            'orientation_covariance': np.array([msg['orientation_covariance'] for msg in imu_data]),
            'magnetometer_x': np.array([msg['magnetometer_x'] for msg in imu_data]),
            'magnetometer_y': np.array([msg['magnetometer_y'] for msg in imu_data]),
            'magnetometer_z': np.array([msg['magnetometer_z'] for msg in imu_data])
        },
        'gps': {
            'timestamps': np.array([msg['timestamp'] for msg in gps_data]),
            'latitude': np.array([msg['latitude'] for msg in gps_data]),
            'longitude': np.array([msg['longitude'] for msg in gps_data]),
            'altitude': np.array([msg['altitude'] for msg in gps_data]),
            'utm_easting': np.array([msg['utm_easting'] for msg in gps_data]),
            'utm_northing': np.array([msg['utm_northing'] for msg in gps_data]),
            'zone': np.array([msg['zone'] for msg in gps_data]),
            'letter': np.array([msg['letter'] for msg in gps_data])
        }
    }

    # Save the data to a .mat file
    savemat(mat_file_path, data, do_compression=True)
    print(f"Data saved to {mat_file_path}")

def main():
    # Inputs from the user
    bag_folder = 'home/shrirag10/LAB4/src/imu_driver/data_cirlces_t.bag'
    imu_topic = Path('imu_msgs/msg/IMUmsg.msg').read_text()
    gps_topic = Path('gps_msgs/msg/GPSmsg.msg').read_text()
    
    mat_file_path = 'imu_driver/circles_t.mat'
    # Check if bag folder exists
    if not os.path.exists(bag_folder):
        raise FileNotFoundError(f"Bag folder {bag_folder} does not exist")

    # Process bag and convert data
    imu_data, gps_data = read_sensor_data_from_bag(bag_folder, imu_topic, gps_topic)
    convert_to_mat(imu_data, gps_data, mat_file_path)

if __name__ == "__main__":
    main()

