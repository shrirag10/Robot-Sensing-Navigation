import csv
import numpy as np
from pathlib import Path
from rosbags.highlevel import AnyReader
from rosbags.typesys import Stores, get_typestore, get_types_from_msg
from tf_transformations import euler_from_quaternion

# Load ROS2 bag data for IMU sensor readings
def load_ros2_bag_data(bagfile):
    imu_data = {'time': [], 'accel': [], 'gyro': [], 'orientation': []}
    
    bagpath = Path(bagfile)
    msg_text = Path('imu_msgs/msg/IMUmsg.msg').read_text()

    # Create a type store
    typestore = get_typestore(Stores.ROS2_HUMBLE)
    add_types = {}
    add_types.update(get_types_from_msg(msg_text, 'imu_msgs/msg/IMUmsg'))

    typestore.register(add_types)
    
    # Reading the data from the bagfile
    with AnyReader([bagpath], default_typestore=typestore) as reader:
        connections = [x for x in reader.connections if x.topic == '/imu']
        for connection, timestamp, rawdata in reader.messages(connections=connections):
            msg = reader.deserialize(rawdata, connection.msgtype)
            
            # Extract accelerometer and gyroscope data
            accel_x = msg.imu.linear_acceleration.x
            accel_y = msg.imu.linear_acceleration.y
            accel_z = msg.imu.linear_acceleration.z

            gyro_x = msg.imu.angular_velocity.x
            gyro_y = msg.imu.angular_velocity.y
            gyro_z = msg.imu.angular_velocity.z

            # Append extracted data to the dictionary
            imu_data['time'].append(timestamp / 1e9)  # Convert nanoseconds to seconds
            imu_data['accel'].append([accel_x, accel_y, accel_z])
            imu_data['gyro'].append([gyro_x, gyro_y, gyro_z])
            imu_data['orientation'].append([msg.imu.orientation.x, msg.imu.orientation.y, msg.imu.orientation.z, msg.imu.orientation.w])
    
    return imu_data

# Convert quaternions to Euler angles
def convert_to_euler(orientations):
    euler_angles = []
    for quat in orientations:
        roll, pitch, yaw = euler_from_quaternion(quat)
        euler_angles.append([roll, pitch, yaw])
    return np.array(euler_angles)

# Save IMU data to a CSV file
def save_to_csv(imu_data, csv_filename):
    euler_angles = convert_to_euler(imu_data['orientation'])

    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write CSV header
        writer.writerow(['time', 'accel_x', 'accel_y', 'accel_z', 
                         'gyro_x', 'gyro_y', 'gyro_z', 
                         'roll', 'pitch', 'yaw'])
        
        # Write the data row by row
        for i in range(len(imu_data['time'])):
            writer.writerow([imu_data['time'][i], 
                             imu_data['accel'][i][0], imu_data['accel'][i][1], imu_data['accel'][i][2],
                             imu_data['gyro'][i][0], imu_data['gyro'][i][1], imu_data['gyro'][i][2],
                             euler_angles[i][0], euler_angles[i][1], euler_angles[i][2]])

# Main function to extract IMU data from rosbag and save to CSV
def convert_bag_to_csv(bag_file, csv_file):
    imu_data = load_ros2_bag_data(bag_file)
    save_to_csv(imu_data, csv_file)
    print(f"Data from {bag_file} has been saved to {csv_file}")

# Example usage
if __name__ == "__main__":
    bag_file = 'imu_driver/fivehour1data.bag'  # Replace with your actual file path
    csv_file = 'imu_data.csv'  # Specify the CSV output file name
    convert_bag_to_csv(bag_file, csv_file)
