import os
import numpy as np
from scipy.io import savemat
from rosbag2_py import StorageOptions, ConverterOptions
from rosbag2_py import SequentialReader
from rclpy.serialization import deserialize_message
from sensor_msgs.msg import Imu

def find_db_file(bag_folder):
    for file in os.listdir(bag_folder):
        if file.endswith('.db3'):
            return os.path.join(bag_folder, file)
    raise FileNotFoundError(f"No .db3 file found in {bag_folder}")

def read_ros2_bag(bag_folder):
    db_path = find_db_file(bag_folder)

    storage_options = StorageOptions(uri=bag_folder, storage_id='sqlite3')
    converter_options = ConverterOptions(
        input_serialization_format='cdr',
        output_serialization_format='cdr'
    )

    reader = SequentialReader()
    reader.open(storage_options, converter_options)

    topic_types = reader.get_all_topics_and_types()
    print("Topics in the bag:")
    for topic_type in topic_types:
        print(f"  - {topic_type.name}: {topic_type.type}")

    imu_messages = []
    message_count = 0
    topic_counts = {}
    
    while reader.has_next():
        (topic, data, t) = reader.read_next()
        message_count += 1
        topic_counts[topic] = topic_counts.get(topic, 0) + 1
        if topic == '/imu':
            msg = deserialize_message(data, Imu)
            imu_messages.append((t, msg))
        
        if message_count % 100000 == 0:
            print(f"Processed {message_count} messages...")

    print(f"\nTotal messages processed: {message_count}")
    for topic, count in topic_counts.items():
        print(f"Messages in {topic}: {count}")
    print(f"IMU messages found: {len(imu_messages)}")
    return imu_messages

def convert_imu_messages_to_mat(imu_messages):
    data = {
        'timestamps': [],
        'angular_velocity_x': [], 'angular_velocity_y': [], 'angular_velocity_z': [],
        'linear_acceleration_x': [], 'linear_acceleration_y': [], 'linear_acceleration_z': [],
        'orientation_x': [], 'orientation_y': [], 'orientation_z': [], 'orientation_w': [],
        'angular_velocity_covariance': [],
        'linear_acceleration_covariance': [],
        'orientation_covariance': []
    }

    for t, msg in imu_messages:
        data['timestamps'].append(t)
        data['angular_velocity_x'].append(msg.angular_velocity.x)
        data['angular_velocity_y'].append(msg.angular_velocity.y)
        data['angular_velocity_z'].append(msg.angular_velocity.z)
        data['linear_acceleration_x'].append(msg.linear_acceleration.x)
        data['linear_acceleration_y'].append(msg.linear_acceleration.y)
        data['linear_acceleration_z'].append(msg.linear_acceleration.z)
        data['orientation_x'].append(msg.orientation.x)
        data['orientation_y'].append(msg.orientation.y)
        data['orientation_z'].append(msg.orientation.z)
        data['orientation_w'].append(msg.orientation.w)
        data['angular_velocity_covariance'].append(msg.angular_velocity_covariance)
        data['linear_acceleration_covariance'].append(msg.linear_acceleration_covariance)
        data['orientation_covariance'].append(msg.orientation_covariance)

    # Convert to numpy arrays with appropriate dtypes
    data['timestamps'] = np.array(data['timestamps'], dtype=np.uint64)
    for key in ['angular_velocity_x', 'angular_velocity_y', 'angular_velocity_z',
                'linear_acceleration_x', 'linear_acceleration_y', 'linear_acceleration_z',
                'orientation_x', 'orientation_y', 'orientation_z', 'orientation_w']:
        data[key] = np.array(data[key], dtype=np.float64)
    for key in ['angular_velocity_covariance', 'linear_acceleration_covariance', 'orientation_covariance']:
        data[key] = np.array(data[key], dtype=np.float64)

    print("\nData shapes:")
    for key, value in data.items():
        print(f"{key}: {value.shape}")

    return data

def main():
    bag_folder = 'imu_driver/fivehourdata.bag'
    mat_file_path = 'output.mat'

    if not os.path.exists(bag_folder):
        raise FileNotFoundError(f"Bag folder {bag_folder} does not exist")

    print(f"Processing bag folder: {bag_folder}")
    imu_messages = read_ros2_bag(bag_folder)
    data = convert_imu_messages_to_mat(imu_messages)

    savemat(mat_file_path, data, do_compression=False)
    print(f"\nData saved to {mat_file_path}")
    print(f"Output file size: {os.path.getsize(mat_file_path) / (1024*1024):.2f} MB")

    # Print original bag file size
    total_bag_size = sum(os.path.getsize(os.path.join(bag_folder, f)) for f in os.listdir(bag_folder) if f.endswith('.db3'))
    print(f"Original bag file size: {total_bag_size / (1024*1024):.2f} MB")

if __name__ == "__main__":
    main()
