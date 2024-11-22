import rosbag2_py
import rclpy.serialization
from gps_msgs.msg import GPSmsg  
import matplotlib.pyplot as plt
import numpy as np

def read_gps_data_from_bag(bag_path, topic_name):
    # Initialize bag reader
    bag_reader = rosbag2_py.SequentialReader()
    storage_options = rosbag2_py.StorageOptions(uri=bag_path, storage_id='sqlite3')
    converter_options = rosbag2_py.ConverterOptions('', '')
    bag_reader.open(storage_options, converter_options)
    latitudes = []
    longitudes = []

    while bag_reader.has_next():
        (topic, data, t) = bag_reader.read_next()
        if topic == topic_name:
            msg = rclpy.serialization.deserialize_message(data, GPSmsg)
            # Append latitude and longitude
            latitudes.append(msg.latitude)
            longitudes.append(msg.longitude)
    return latitudes, longitudes

bag_path = '/home/shrirag10/ros2_ws_lab1/walking_data/walking_data_0.db3'  
topic_name = '/gps'  
latitudes, longitudes = read_gps_data_from_bag(bag_path, topic_name)
latitudes = np.array(latitudes)
longitudes = np.array(longitudes)
z = np.polyfit(longitudes, latitudes, 1)  
p = np.poly1d(z) 
plt.figure(figsize=(10, 6))

plt.scatter(longitudes, latitudes, color='blue', label='Observed GPS', s=10)
plt.plot(longitudes, p(longitudes), color='red', label='Trendline')
plt.title('Latitude vs Longitude Plot from GPS Data with Trendline')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid(True)
plt.legend()
plt.show()
