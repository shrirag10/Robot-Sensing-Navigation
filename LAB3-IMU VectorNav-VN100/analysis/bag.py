from pathlib import Path
from rosbags.highlevel import AnyReader
from rosbags.typesys import Stores, get_typestore, get_types_from_idl, get_types_from_msg
from tf_transformations import euler_from_quaternion
import matplotlib.pyplot as plt
import numpy as np

MAG_G_TO_T = 1e-4  # Conversion factor from Gauss to Tesla

# Step 1: Load ros2 db3 file and extract /imu topic data
def load_ros2_bag_data(bagfile):
    imu_data = {'time': [], 'accel': [], 'gyro': [], 'orientation': [], 'mag_field': []}
    
    bagpath = Path(bagfile)
    msg_text = Path('imu_msgs/msg/IMUmsg.msg').read_text()

    # Create a type store to use if the bag has no message definitions.
    typestore = get_typestore(Stores.ROS2_HUMBLE)

    add_types = {}
    add_types.update(get_types_from_msg(msg_text, 'imu_msgs/msg/IMUmsg'))
    typestore.register(add_types)

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

            # Extract magnetic field data (converted to Tesla)
            mag_x = msg.mag_field.magnetic_field.x * MAG_G_TO_T
            mag_y = msg.mag_field.magnetic_field.y * MAG_G_TO_T
            mag_z = msg.mag_field.magnetic_field.z * MAG_G_TO_T

            # Print extracted values to debug
            print(f"Accel (x, y, z): {accel_x}, {accel_y}, {accel_z}")
            print(f"Gyro (x, y, z): {gyro_x}, {gyro_y}, {gyro_z}")
            print(f"Magnetic Field (x, y, z) [Tesla]: {mag_x}, {mag_y}, {mag_z}")

            # Append extracted data
            imu_data['time'].append(timestamp / 1e9)  # Convert nanoseconds to seconds
            imu_data['accel'].append([accel_x, accel_y, accel_z])
            imu_data['gyro'].append([gyro_x, gyro_y, gyro_z])
            imu_data['orientation'].append([msg.imu.orientation.x, msg.imu.orientation.y, 
                                            msg.imu.orientation.z, msg.imu.orientation.w])
            imu_data['mag_field'].append([mag_x, mag_y, mag_z])
    
    return imu_data

# Step 2: Convert quaternions to Euler angles
def convert_to_euler(orientations):
    euler_angles = []
    for quat in orientations:
        roll, pitch, yaw = euler_from_quaternion(quat)
        euler_angles.append([roll, pitch, yaw])
    return np.array(euler_angles)

# Step 3: Compute noise statistics
def compute_statistics(data):
    data_np = np.array(data)
    mean = np.mean(data_np, axis=0)
    std_dev = np.std(data_np, axis=0)
    return mean, std_dev

# Step 4: Plot time-series and histograms
def plot_time_series(time, data, title, ylabel):
    plt.figure(figsize=(10, 6))
    plt.plot(time, data)
    plt.title(title)
    plt.xlabel("Time [s]")
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()

def plot_histogram(data, title, xlabel):
    plt.figure(figsize=(8, 6))
    plt.hist(data, bins=50, alpha=0.75)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()

# Main function to analyze ros2 bag data
def analyze_imu_data(db3_file):
    imu_data = load_ros2_bag_data(db3_file)
    
    # Convert orientation quaternions to Euler angles
    euler_angles = convert_to_euler(imu_data['orientation'])
    
    # Calculate statistics
    accel_mean, accel_std = compute_statistics(imu_data['accel'])
    gyro_mean, gyro_std = compute_statistics(imu_data['gyro'])
    euler_mean, euler_std = compute_statistics(euler_angles)
    mag_mean, mag_std = compute_statistics(imu_data['mag_field'])

    # Print statistics
    print(f"Accelerometer Mean: {accel_mean}, Std Dev: {accel_std}")
    print(f"Gyroscope Mean: {gyro_mean}, Std Dev: {gyro_std}")
    print(f"Euler Angles Mean: {euler_mean}, Std Dev: {euler_std}")
    print(f"Magnetic Field Mean [Tesla]: {mag_mean}, Std Dev: {mag_std}")

    # Plot time series data for Linear Acceleration
    for i, axis in enumerate(['X', 'Y', 'Z']):
        plot_time_series(imu_data['time'], np.array(imu_data['accel'])[:, i], 
                         f'Linear Acceleration - {axis}', f'Acceleration {axis} [m/s²]')
        plot_histogram(np.array(imu_data['accel'])[:, i], 
                       f'Linear Acceleration Histogram - {axis}', f'Acceleration {axis} [m/s²]')

    # Plot time series data for Angular Velocity
    for i, axis in enumerate(['X', 'Y', 'Z']):
        plot_time_series(imu_data['time'], np.array(imu_data['gyro'])[:, i], 
                         f'Angular Velocity - {axis}', f'Angular Velocity {axis} [rad/s]')
        plot_histogram(np.array(imu_data['gyro'])[:, i], 
                       f'Angular Velocity Histogram - {axis}', f'Angular Velocity {axis} [rad/s]')

    # Plot time series data for Magnetic Field
    for i, axis in enumerate(['X', 'Y', 'Z']):
        plot_time_series(imu_data['time'], np.array(imu_data['mag_field'])[:, i], 
                         f'Magnetic Field - {axis}', f'Magnetic Field {axis} [Tesla]')
        plot_histogram(np.array(imu_data['mag_field'])[:, i], 
                       f'Magnetic Field Histogram - {axis}', f'Magnetic Field {axis} [Tesla]')

    # Plot time series data for Euler Angles (Yaw, Pitch, Roll)
    for i, axis in enumerate(['Roll', 'Pitch', 'Yaw']):
        plot_time_series(imu_data['time'], euler_angles[:, i], 
                         f'Euler Angles - {axis}', f'{axis} [rad]')
        plot_histogram(euler_angles[:, i], f'Euler Angles Histogram - {axis}', f'{axis} [rad]')

# Example usage
if __name__ == "__main__":
    bag_file = 'imu_driver/stationarydata.bag'
    analyze_imu_data(bag_file)

