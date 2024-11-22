import matplotlib.pyplot as plt
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

# Compute Allan deviation
def compute_allan_deviation(data, dt):
    N = len(data)
    max_tau = N // 2
    tau_values = np.logspace(np.log10(1), np.log10(max_tau), num=50).astype(int)

    allan_dev = []
    for tau in tau_values:
        avgs = [np.mean(data[i:i + tau]) for i in range(0, N - tau, tau)]
        adev = np.sqrt(0.5 * np.mean(np.diff(avgs) ** 2))
        allan_dev.append(adev)
    
    return tau_values * dt, np.array(allan_dev)  # Convert to NumPy array

# Function to plot Allan deviation for accelerometer and gyroscope separately
def plot_separate_allan_variance(tau, allan_dev_accel, allan_dev_gyro):
    # Plotting for Accelerometer
    plt.figure(figsize=(10, 8))  # Adjust figure size for better visibility
    plt.loglog(tau, allan_dev_accel, label='Combined Accelerometer Axes', color='b')

    # Set axis limits for accelerometer
    plt.xlim(1e-2, 1e6)
    plt.ylim(1e-4, 1e4)

    plt.title("Allan Deviation for Accelerometer", fontsize=14)
    plt.xlabel(r'$\tau$ (s)', fontsize=12)
    plt.ylabel(r'$\sigma(\tau)$', fontsize=12)

    plt.grid(True, which="both", ls="--", lw=0.5)  # Dotted lines for grid
    plt.minorticks_on()
    plt.legend(loc='best')
    plt.show()

    # Plotting for Gyroscope
    plt.figure(figsize=(10, 8))  # Adjust figure size for better visibility
    plt.loglog(tau, allan_dev_gyro, label='Combined Gyroscope Axes', color='g')

    # Set axis limits for gyroscope
    plt.xlim(1e-2, 1e6)

    # Adjust the y-axis limits based on the observed data range for gyroscope
    min_y_gyro = np.min(allan_dev_gyro[allan_dev_gyro > 0]) * 0.1  # Set a minimum limit based on data
    max_y_gyro = np.max(allan_dev_gyro) * 10  # Set a maximum limit based on data
    plt.ylim(min_y_gyro, max_y_gyro)

    plt.title("Allan Deviation for Gyroscope", fontsize=14)
    plt.xlabel(r'$\tau$ (s)', fontsize=12)
    plt.ylabel(r'$\sigma(\tau)$', fontsize=12)

    plt.grid(True, which="both", ls="--", lw=0.5)
    plt.minorticks_on()
    plt.legend(loc='best')
    plt.show()

# Combine accelerometer and gyroscope axes data
def combine_axes_data(imu_data, sensor_type):
    combined_data = np.linalg.norm(np.array(imu_data[sensor_type]), axis=1)
    return combined_data

# Main function to analyze ros2 bag data
def analyze_imu_data(db3_file):
    imu_data = load_ros2_bag_data(db3_file)
    
    # Sampling time interval (assuming uniform sampling)
    dt = np.mean(np.diff(imu_data['time']))
    
    # Combine X, Y, Z axes for accelerometer and gyroscope
    combined_accel_data = combine_axes_data(imu_data, 'accel')
    combined_gyro_data = combine_axes_data(imu_data, 'gyro')

    # Calculate Allan deviation for combined accelerometer and gyroscope data
    tau, allan_dev_accel = compute_allan_deviation(combined_accel_data, dt)
    tau, allan_dev_gyro = compute_allan_deviation(combined_gyro_data, dt)

    # Plot separate Allan variance for accelerometer and gyroscope
    plot_separate_allan_variance(tau, allan_dev_accel, allan_dev_gyro)

# Example usage
if __name__ == "__main__":
    bag_file = 'imu_driver/fivehour1data.bag'  # Replace with your actual file path
    analyze_imu_data(bag_file)

