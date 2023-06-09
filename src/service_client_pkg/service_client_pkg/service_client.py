#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from service_pkg.srv import CustomService

class ServiceClientNode(Node):
    def __init__(self):
        super().__init__('service_client_node')

        # Clients for 2 custom services
        self.client1 = self.create_client(CustomService, 'service1')
        self.client2 = self.create_client(CustomService, 'service2')

        # Publisher for response messages
        self.publisher = self.create_publisher(Float32, 'response_topic', 10)

        # Service call at 500 Hz
        self.timer = self.create_timer(1.0 / 500, self.timer_callback) 

    def timer_callback(self):
        # Triggers service calls 
        self.call_service(self.client1)
        self.call_service(self.client2)

    def call_service(self, client):
        # Wait for service to become available
        if not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('Service not available')
            return

        # Send a request 
        request = CustomService.Request()
        future = client.call_async(request)
        future.add_done_callback(self.service_callback)

    def service_callback(self, future):
        try:
            response = future.result()
            self.publish_response(response.filtered_data)
        except Exception as e:
            self.get_logger().error('Service call failed: %s' % str(e))

    def publish_response(self, filtered_data):
        # Publish filtered data from service response as as topic
        msg = Float32()
        msg.data = filtered_data
        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = ServiceClientNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
