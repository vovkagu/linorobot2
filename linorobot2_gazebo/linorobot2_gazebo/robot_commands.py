import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time
import math

class RobotCommandNode(Node):
    def __init__(self):
        super().__init__('robot_command_node')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info('Robot Command Node started. Waiting for commands...')

    def move_straight(self, distance):
        self.get_logger().info(f'Moving straight {distance} meters')
        msg = Twist()
        msg.linear.x = 0.2  # constant speed
        
        duration = distance / msg.linear.x
        start_time = time.time()
        
        while (time.time() - start_time) < duration:
            self.publisher_.publish(msg)
            time.sleep(0.1)
        
        self.stop_robot()

    def turn(self, angle_degrees):
        self.get_logger().info(f'Turning {angle_degrees} degrees')
        msg = Twist()
        # Positive angle = left turn (counter-clockwise)
        msg.angular.z = 0.5 if angle_degrees > 0 else -0.5
        
        angle_rad = math.radians(abs(angle_degrees))
        duration = angle_rad / abs(msg.angular.z)
        start_time = time.time()
        
        while (time.time() - start_time) < duration:
            self.publisher_.publish(msg)
            time.sleep(0.1)
            
        self.stop_robot()

    def stop_robot(self):
        msg = Twist()
        self.publisher_.publish(msg)
        self.get_logger().info('Robot stopped')

def main(args=None):
    rclpy.init(args=args)
    node = RobotCommandNode()
    
    # This node will be driven by the MCP server via a service or simple logic
    # For the initial implementation, we'll leave it as a class that can be imported 
    # or converted to a service node.
    
    # To make it usable by MCP, let's turn it into a Service node.
    # Since I cannot run a full MCP server in this environment without specific dependencies,
    # I will first implement the ROS 2 side as a service provider.
    
    # Wait... the user wants an MCP server. I should implement a python script that 
    # uses the mcp library and rclpy.
    
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
