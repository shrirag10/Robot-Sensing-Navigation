from pathlib import Path
from rosbags.highlevel import AnyReader
from rosbags.typesys import Stores, get_typestore, get_types_from_idl, get_types_from_msg
from tf_transformations import euler_from_quaternion
import matplotlib.pyplot as plt
import numpy as np
import allan_variance
from scipy import integrate, signal
         
# Step 1: Load ros2 db3 file and extract /imu topic data
def load_ros2_bag_data(bagfile):
    imu_data = {'time': [], 'accel': [], 'gyro': [], 'orientation': [], 'mag': []}
    gps_data = {'time': [], 'easting':[],'northing':[],'zone':[],'letter':[]}
    
    bagpath = Path(bagfile)

    imu_text = Path('imu_msgs/msg/IMUmsg.msg').read_text()
    gps_text = Path('gps_msgs/msg/GPSmsg.msg').read_text()

    # Create a type store to use if the bag has no message definitions.
    typestore = get_typestore(Stores.ROS2_HUMBLE)

    add_types = {}
    add_types.update(get_types_from_msg(imu_text, 'imu_msgs/msg/IMUmsg'))
    add_types.update(get_types_from_msg(gps_text, 'gps_msgs/msg/GPSmsg'))
    tesla_to_milligauss= 1e7
    typestore.register(add_types)
    with AnyReader([bagpath], default_typestore=typestore) as reader:
        imu_connections = [x for x in reader.connections if x.topic == '/imu']
        gps_connections = [y for y in reader.connections if y.topic == '/gps']

        for connection, timestamp, rawdata in reader.messages(connections=imu_connections):
            msg = reader.deserialize(rawdata, connection.msgtype)
        
            # Extract accelerometer and gyroscope data
            accel_x = msg.imu.linear_acceleration.x
            accel_y = msg.imu.linear_acceleration.y
            accel_z = msg.imu.linear_acceleration.z

            gyro_x = msg.imu.angular_velocity.x
            gyro_y = msg.imu.angular_velocity.y
            gyro_z = msg.imu.angular_velocity.z

            mag_x = msg.mag_field.magnetic_field.x
            mag_y = msg.mag_field.magnetic_field.y
            mag_z = msg.mag_field.magnetic_field.z

            time_s = msg.header.stamp.sec
            time_ns = msg.header.stamp.nanosec
            time = time_s + time_ns/1e9

            # Append extracted data
            imu_data['time'].append(time)
            imu_data['accel'].append([accel_x, accel_y, accel_z])
            imu_data['gyro'].append([gyro_x, gyro_y, gyro_z])
            imu_data['orientation'].append([msg.imu.orientation.x, msg.imu.orientation.y, msg.imu.orientation.z, msg.imu.orientation.w])
            imu_data['mag'].append([mag_x, mag_y, mag_z])
        
        for connection, timestamp, rawdata in reader.messages(connections=gps_connections):
            msg = reader.deserialize(rawdata, connection.msgtype)

            # Extract UTM data
            utm_easting = msg.utm_easting
            utm_northing = msg.utm_northing
            utm_zone = msg.zone
            utm_letter = msg.letter

            time_s = msg.header.stamp.sec
            time_ns = msg.header.stamp.nanosec
            time = time_s + time_ns/1e9

            # Append extracted data
            gps_data['time'].append(time)
            gps_data['easting'].append(utm_easting)
            gps_data['northing'].append(utm_northing)
            gps_data['zone'].append(utm_zone)
            gps_data['letter'].append(utm_letter)

    return imu_data, gps_data

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

def get_magcal_matrix(mag_data):
    mag_data_np = np.array(mag_data)
    meanx = np.mean(mag_data_np[:,0])
    meany = np.mean(mag_data_np[:,1])

    x = mag_data_np[:,0].T
    y = mag_data_np[:,1].T

    D = np.c_[x**2, x*y, y**2, x, y, np.ones_like(x)]
    S = np.dot(D.T, D)

    eigvals, eigvecs = np.linalg.eig(S)
    min_eigval_index = np.argmin(eigvals)
    ellipse_params = eigvecs[:, min_eigval_index]
    
    center_x = -ellipse_params[3] / (2 * ellipse_params[0])
    center_y = -ellipse_params[4] / (2 * ellipse_params[2])
    
    xh = x - center_x
    yh = y - center_y

    Dh = np.c_[xh**2, xh*yh, yh**2, xh, yh, np.ones_like(xh)]
    Sh = np.dot(Dh.T, Dh)
    evalsh, evecsh = np.linalg.eig(Sh)
    min_eigvalh_index = np.argmin(evalsh)
    ellipseh_params = evecsh[:, min_eigvalh_index]

    # Semi-major and semi-minor axes
    semi_major = np.sqrt(1 / ellipseh_params[0])  # Semi-major axis
    semi_minor = np.sqrt(1 / ellipseh_params[2])  # Semi-minor axis

    # Calculate rotation angle
    rotation = 0.5 * np.arctan2(ellipseh_params[1], ellipseh_params[0] - ellipseh_params[2])

    scale_x = 1 / semi_major
    scale_y = 1 / semi_minor

    # Homography matrix
    H = np.array([
        [scale_x * np.cos(rotation), -scale_y * np.sin(rotation), 0],
        [scale_x * np.sin(rotation), scale_y * np.cos(rotation), 0],
        [0, 0, 1]
    ])

    return H, center_x, center_y
    

# Step 4: Plot time-series and histograms
def plot_time_series(time, data, title, ylabel):
    plt.figure(figsize=(10, 6))
    plt.plot(time, data)
    plt.title(title)
    plt.xlabel("Time [s]")
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()

def plot_magcal(x, y, xcenter, ycenter, xcal, ycal, title, xlabel, ylabel):
    plt.figure(figsize=(8, 8))
    plt.scatter(x, y, color='blue', label='Raw Mag Data')
    plt.scatter(xcenter,ycenter, color='red')
    plt.scatter(xcal,ycal, color='purple', label='Calibrated Mag Data')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_histogram(data, title, xlabel):
    plt.figure(figsize=(8, 6))
    plt.hist(data, bins=50, alpha=0.75)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()

def plot_allan_deviation(data, title):
    plt.figure(figsize=(10,6))
    dt = 1 / 40
    tau, avar = allan_variance.compute_avar(data,dt)
    plt.loglog(tau, avar, '.')
    plt.xlabel("Averaging time, s")
    plt.ylabel("Allan Variance")
    plt.title(title)
    plt.grid(True)
    plt.show()

def plot_time_series_comparison(time, data1, label1, data2, label2, title, ylabel):
    plt.figure(figsize=(10, 6))
    plt.plot(time, data1, label=label1)
    plt.plot(time, data2, label=label2)
    plt.title(title)
    plt.xlabel("Time [s]")
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_3_time_series(time, data1, label1, data2, label2, data3, label3, title, ylabel):
    plt.figure(figsize=(10, 6))
    plt.plot(time, data1, label=label1)
    plt.plot(time, data2, label=label2)
    plt.plot(time, data3, label=label3)
    plt.title(title)
    plt.xlabel("Time [s]")
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_velocity_comparison(imu_time, imu_vel, gps_time, gps_vel):
    plt.figure()
    plt.scatter(imu_time,imu_vel,label="IMU Forward Velocity")
    plt.scatter(gps_time, gps_vel, label="GPS Forward Velocity", color='orange')
    plt.title("Forward Velocities Calculated from IMU and GPS data")
    plt.xlabel("Time [s]")
    plt.ylabel("Velocity [m/s]")
    plt.grid(True)
    plt.legend()
    plt.show()

def wrap_to_pi(data):
    data_wrapped_to_pi = np.remainder(data, 2*np.pi)
    mask = np.abs(data_wrapped_to_pi)>np.pi
    data_wrapped_to_pi[mask] -= 2*np.pi*np.sign(data_wrapped_to_pi[mask])
    return data_wrapped_to_pi


def butter_lowpass(cutoff, fs, order=5):
    return signal.butter(order, cutoff, fs=fs, btype='low', analog=False)

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = signal.lfilter(b, a, data)
    return y


def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, fs=fs, btype='high', analog=False)
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y

def complementary_filter(gyro_data, mag_data, alpha=0.98):
    filtered_angle = np.zeros_like(mag_data)
    for i in range(1, len(gyro_data)):
        filtered_angle[i] = (alpha * (gyro_data[i]) +
                             (1 - alpha) * mag_data[i])
    return filtered_angle

def gps_forward_velocity(time, easting, northing):
    velocities = [0]
    epsilon = 1e-9  # Small value to avoid division by zero

    for i in range(1, len(easting)):
        dt = time[i] - time[i - 1] + epsilon  # Adding epsilon to avoid zero division
        distance = np.sqrt((easting[i] - easting[i - 1])**2 + (northing[i] - northing[i - 1])**2)
        velocity = distance / dt
        velocities.append(velocity)
    return velocities


def imu_forward_velocity(time, for_acc):
    velocities = [0]
    for i in range(1, len(for_acc)):
        dt = time[i]-time[i-1]
        velocity = velocities[i-1] + 0.5 *for_acc[i] * dt
        velocities.append(velocity)
    return velocities
    
###################    
# Function to compute East and North velocities based on yaw and forward velocity
def compute_trajectory_with_heading(yaw_angles, forward_velocity):
    ve = forward_velocity * np.cos(yaw_angles)  # Eastward velocity component
    vn = forward_velocity * np.sin(yaw_angles)  # Northward velocity component
    return ve, vn

# Function to integrate velocity to obtain displacement in East and North directions
def integrate_displacement(ve, vn, time):
    xe = integrate.cumulative_trapezoid(ve, time, initial=0)  # Displacement in East
    xn = integrate.cumulative_trapezoid(vn, time, initial=0)  # Displacement in North
    return xe, xn



# Main function to analyze ros2 bag data
def analyze_imu_data(circlebag, drivingbag):
    circle_imu_data, circle_gps_data = load_ros2_bag_data(circlebag)
    driving_imu_data, driving_gps_data = load_ros2_bag_data(drivingbag)
    
    # Magnetometer Calibration
    calibration_matrix, center_x, center_y = get_magcal_matrix(circle_imu_data['mag'])
    xc = np.array(circle_imu_data['mag'])[:,0]
    yc = np.array(circle_imu_data['mag'])[:,1]
    circle_calibrated_coords = calibration_matrix@(np.vstack([xc-center_x,yc-center_y,np.ones_like(xc).T]))
    
    plot_magcal(xc, yc, center_x, center_y, circle_calibrated_coords[0], circle_calibrated_coords[1],"Circle Driving Magnetometer Data (Raw and Calibrated)","MagX (T)","MagY (T)")

    xd = np.array(driving_imu_data['mag'])[:,0]
    yd = np.array(driving_imu_data['mag'])[:,1]
    raw_yaw = np.arctan2(xd, yd)
    driving_calibrated_coords = calibration_matrix@(np.vstack([xd-center_x,yd-center_y,np.ones_like(xd).T]))
    calibrated_yaw = np.arctan2(driving_calibrated_coords[0], driving_calibrated_coords[1])

    plot_time_series_comparison(driving_imu_data['time'],raw_yaw, "Yaw Angle from Raw Data", calibrated_yaw, "Yaw Angle from Calibrated Data", "Yaw Angle from Magnetometer Data", "Yaw (rad)")

    gyroZ = np.array(driving_imu_data['gyro'])[:,2]
    yaw_from_gyro = integrate.cumulative_trapezoid(gyroZ,driving_imu_data['time'],initial=0)
    yaw_from_gyro = yaw_from_gyro-(yaw_from_gyro[0]-calibrated_yaw[0])
    yaw_from_gyro_final = wrap_to_pi(yaw_from_gyro)
    plot_time_series_comparison(driving_imu_data['time'],yaw_from_gyro_final, "Yaw Angle Integrated from Gyro", calibrated_yaw, "Yaw Angle from Calibrated Magnetometer Data", "Yaw Angle from Gyro vs. Magnetometer Data", "Yaw (rad)")
    

    alpha = 0.9
    gyro_hpf = alpha * yaw_from_gyro_final
    mag_lpf = (1 - alpha) * calibrated_yaw

    filtered_data = wrap_to_pi(gyro_hpf + mag_lpf)
    plot_3_time_series(driving_imu_data['time'],mag_lpf, "Calibrated Magnetometer Data Through Low Pass Filter", gyro_hpf, "Integrated Gyroscope Data Through High Pass Filter", filtered_data, "Complementary Filter", "Filtered Data", "Yaw (rad)")

    euler_angles = convert_to_euler(driving_imu_data['orientation'])
    imu_yaw = np.array(euler_angles)[:,2]
    imu_yaw = wrap_to_pi(imu_yaw-(imu_yaw[0]-filtered_data[0]))
    plot_time_series_comparison(driving_imu_data['time'], imu_yaw, "IMU Yaw Reading", filtered_data, "Complementary Filter Yaw Estimate", "Estimated Yaw vs. IMU Yaw", "Yaw(rad)")

    for_acc = np.array(driving_imu_data['accel'])[:,0]   #Changed to flip the direction
    for_acc = butter_lowpass_filter(for_acc,0.5,40)
    
    for_vel_imu = imu_forward_velocity(driving_imu_data['time'],for_acc=for_acc)
    for_vel_gps = gps_forward_velocity(driving_gps_data['time'],driving_gps_data['easting'],driving_gps_data['northing'])
    plot_time_series(driving_imu_data['time'],for_acc,"Acceleration","m/s^2")
    plot_velocity_comparison(driving_imu_data['time'], for_vel_imu, driving_gps_data['time'], for_vel_gps)
#################################
    # Compute yaw from gyroscope and magnetometer data with complementary filtering
    alpha = 0.9
    gyro_yaw = wrap_to_pi(yaw_from_gyro)  # Yaw integrated from gyro data
    mag_yaw = wrap_to_pi(calibrated_yaw)  # Yaw calculated from magnetometer data
    fused_yaw = wrap_to_pi(alpha * gyro_yaw + (1 - alpha) * mag_yaw)  # Complementary filter

    # Plot yaw comparison after filtering
    plot_3_time_series(
        driving_imu_data['time'], mag_yaw, "Magnetometer (Low Pass)",
        gyro_yaw, "Gyroscope (High Pass)", fused_yaw, "Fused Yaw (Complementary Filter)",
        "Fused Yaw Data", "Yaw (rad)"
    )
        # Step 7: Dead Reckoning Trajectory Estimation with IMU and GPS Alignment
    # Calculate East and North components of velocity using yaw angles and forward velocity
    ve, vn = compute_trajectory_with_heading(fused_yaw, for_vel_imu)
    
    # Integrate velocities to get East and North displacements
    xe, xn = integrate_displacement(ve, vn, driving_imu_data['time'])

    # Plot estimated IMU trajectory alongside GPS trajectory
    plt.figure(figsize=(10, 6))
    plt.plot(xe, xn, label="IMU Estimated Trajectory", color='blue')
    plt.plot(driving_gps_data['easting'], driving_gps_data['northing'], linestyle='--', color='orange', label="GPS Trajectory")
    plt.title("Dead Reckoning Trajectory Comparison: IMU vs GPS")
    plt.xlabel("Easting [m]")
    plt.ylabel("Northing [m]")
    plt.grid(True)
    plt.legend()
    plt.show()

    

# Example usage
if __name__ == "__main__":
    cirlce_bag_file = 'imu_driver/data_going_in_circles.bag'
    driving_bag_file = 'imu_driver/data_driving.bag'
    analyze_imu_data(cirlce_bag_file, driving_bag_file)

