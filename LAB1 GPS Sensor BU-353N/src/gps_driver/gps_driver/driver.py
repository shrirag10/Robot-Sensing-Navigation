import serial
import sys
import utm
import rclpy
from rclpy.node import Node
from std_msgs.msg import Header
from gps_msgs.msg import GPSmsg
from builtin_interfaces.msg import Time

def convert_to_decimal(degrees_minutes, direction):
    degrees = int(degrees_minutes[:2])
    minutes = float(degrees_minutes[2:])
    decimal_degrees = degrees + (minutes / 60)
    if direction in ['S', 'W']:
        decimal_degrees = -decimal_degrees
    return decimal_degrees

def parse_gpgga(gpgga_sentence):
    if gpgga_sentence.startswith('$GPGGA'):
        parts = gpgga_sentence.split(',')
        if len(parts) > 14:
            time_utc = parts[1]
            try:

                latitude = convert_to_decimal(parts[2], parts[3])
                longitude = convert_to_decimal(parts[4], parts[5])
                altitude = float(parts[9]) if parts[9] else None
                return time_utc, latitude, longitude, altitude
            except ValueError:
                return None
    return None

class GPSPublisher(Node):
    def __init__(self):
        super().__init__('gps_publisher')

        # Declare serial port as a parameter
        self.declare_parameter("port", "/dev/ttyUSB0")
        self.declare_parameter("baudrate", 4800)
        self.declare_parameter("sampling_rate", 10.0)

        custom_port = self.parse_command_line_args()

        serial_port = custom_port if custom_port else self.get_parameter("port").get_parameter_value().string_value
        serial_baud = self.get_parameter("baudrate").value
        sampling_rate = self.get_parameter("sampling_rate").value

        if serial_port is None:
            self.get_logger().error("No serial port specified.")
            rclpy.shutdown()
            return

        # Open the serial port
        try:
            self.port = serial.Serial(serial_port, serial_baud, timeout=3.0)
            self.get_logger().info(f"Using GPS device on port {serial_port} at {serial_baud} baud.")
        except serial.SerialException as e:
            self.get_logger().error(f"Could not open port {serial_port}: {e}")
            rclpy.shutdown()
            return

        self.publisher_ = self.create_publisher(GPSmsg, 'gps', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.last_gpgga_time = self.get_clock().now()

    def parse_command_line_args(self):
        for arg in sys.argv:
            if arg.startswith("port:"):
                return arg.split(":")[1]
        return None

    def timer_callback(self):
        if not self.port:
            self.get_logger().warn("Serial port is not initialized.")
            return

        try:
            line = self.port.readline().decode('ascii', errors='replace').strip()
        except serial.SerialException as e:
            self.get_logger().error(f"Error reading from serial port: {e}")
            return

        if line.startswith('$GPGGA'):
            self.get_logger().info(f"Raw GPS Data: {line}")
            parsed_data = parse_gpgga(line)
            
            if parsed_data:
                time_utc, latitude, longitude, altitude = parsed_data
                utm_coords = utm.from_latlon(latitude, longitude)

                msg = GPSmsg()
                hours = int(time_utc[0:2])
                minutes = int(time_utc[2:4])
                seconds = float(time_utc[4:])
                gps_time = Time()
                gps_time.sec = int(hours*3600 + minutes*60 + int(seconds))
                gps_time.nanosec = 0
                msg.header = Header()
                msg.header.stamp = gps_time
                msg.header.frame_id = "GPS1_Frame"
                msg.latitude = latitude
                msg.longitude = longitude
                msg.altitude = altitude if altitude is not None else float('nan')
                msg.utm_easting = utm_coords[0]
                msg.utm_northing = utm_coords[1]
                msg.zone = utm_coords[2]
                msg.letter = utm_coords[3] # Convert char to ASCII value

                self.publisher_.publish(msg)
                self.get_logger().info(f"Published Data: Lat: {latitude}, Lon: {longitude}, Alt: {altitude}")
                self.last_gpgga_time = self.get_clock().now()

        if (self.get_clock().now() - self.last_gpgga_time).nanoseconds > 5e9:
            self.get_logger().warn("Warning: No $GPGGA sentence received for over 5 seconds.")

def main(args=None):
    rclpy.init(args=args)
    gps_publisher = GPSPublisher()
    
    if gps_publisher.port:  # Proceed only if serial port was initialized
        try:
            rclpy.spin(gps_publisher)
        except KeyboardInterrupt:
            pass
        finally:
            gps_publisher.destroy_node()
            rclpy.shutdown()
    else:
        gps_publisher.get_logger().error("GPS publisher failed to start due to serial port error.")

if __name__ == '_main_':
    main()
