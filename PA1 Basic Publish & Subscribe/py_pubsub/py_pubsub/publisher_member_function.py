
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.9  # Time period
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hi Robotics World !!!: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing message: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal = MinimalPublisher()
    rclpy.spin(minimal)
    minimal.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

