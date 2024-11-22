import rosbag2_py
import rclpy
from rclpy.serialization import deserialize_message
from gps_msgs.msg import GPSmsg 
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

def read_gps_data_from_bag(bag_path, topic_name):
    bag_reader = rosbag2_py.SequentialReader()
    storage_options = rosbag2_py.StorageOptions(uri=bag_path, storage_id='sqlite3')
    converter_options = rosbag2_py.ConverterOptions('', '')
    bag_reader.open(storage_options, converter_options)

    gps_data = []
    while bag_reader.has_next():
        (topic, data, t) = bag_reader.read_next()
        if topic == topic_name:
            msg = deserialize_message(data, GPSmsg)
            gps_data.append({
                'timestamp': msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9,  # Convert to seconds
                'latitude': msg.latitude,
                'longitude': msg.longitude,
                'altitude': msg.altitude,
                'utm_easting': msg.utm_easting,
                'utm_northing': msg.utm_northing,
                'zone': msg.zone,
                'letter': msg.letter
            })
    return gps_data

def plot_utm_data_with_trendline(gps_data):
    utm_eastings = np.array([data['utm_easting'] for data in gps_data])
    utm_northings = np.array([data['utm_northing'] for data in gps_data])
    model = LinearRegression()
    utm_eastings_reshaped = utm_eastings.reshape(-1, 1)  # Reshape for scikit-learn
    model.fit(utm_eastings_reshaped, utm_northings)
    predicted_northings = model.predict(utm_eastings_reshaped)
    plt.figure()
    plt.scatter(utm_eastings, utm_northings, c='blue', label='UTM Points')
    plt.plot(utm_eastings, predicted_northings, color='red', label='Trendline (Mean Line)')
    plt.xlabel('UTM Easting (meters)')
    plt.ylabel('UTM Northing (meters)')
    plt.title('Scatter Plot: UTM Easting vs Northing with Trendline')
    plt.grid(True)
    plt.legend()
    plt.show()
 
if __name__ == "__main__":
    # Path to your ROS2 bag file
    bag_path = "/home/shrirag10/ros2_ws_lab1/walking_data/walking_data_0.db3"
    topic_name = "/gps"
    gps_data = read_gps_data_from_bag(bag_path, topic_name)
    if gps_data:

        plot_utm_data_with_trendline(gps_data)
    else:
        print(f"No GPS data found for topic '{topic_name}' in the bag file.")
