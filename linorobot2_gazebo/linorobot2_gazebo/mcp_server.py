import asyncio
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from mcp.server.fastmcp import FastMCP
import time
import math

# Initialize FastMCP server
mcp = FastMCP("RobotController")

# ROS 2 Node for publishing to /cmd_vel
class RobotCmdNode(Node):
    def __init__(self):
        super().__init__('mcp_robot_controller')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)

    def publish_twist(self, linear_x=0.0, angular_z=0.0, duration=0.0):
        msg = Twist()
        msg.linear.x = linear_x
        msg.angular.z = angular_z
        
        start_time = time.time()
        while (time.time() - start_time) < duration:
            self.publisher_.publish(msg)
            time.sleep(0.1)
        
        # Stop robot
        self.publisher_.publish(Twist())

# Global node instance
ros_node = None

@mcp.tool()
async def move_straight(distance: float):
    """Move the robot straight by a specified distance in meters."""
    global ros_node
    speed = 0.2
    duration = distance / speed
    ros_node.publish_twist(linear_x=speed, duration=duration)
    return f"Moved straight {distance} meters."

@mcp.tool()
async def turn(angle_degrees: float):
    """Turn the robot by a specified angle in degrees. Positive for left, negative for right."""
    global ros_node
    speed = 0.5
    angle_rad = math.radians(abs(angle_degrees))
    direction = 1.0 if angle_degrees > 0 else -1.0
    duration = angle_rad / abs(speed)
    ros_node.publish_twist(angular_z=speed * direction, duration=duration)
    return f"Turned {angle_degrees} degrees."

async def main():
    global ros_node
    # Initialize ROS 2
    rclpy.init()
    ros_node = RobotCmdNode()
    
    # Run MCP server
    # Note: In a real setup, you'd run rclpy.spin in a separate thread
    import threading
    spin_thread = threading.Thread(target=rclpy.spin, args=(ros_node,), daemon=True)
    spin_thread.start()
    
    try:
        # Start MCP server on stdio
        await mcp.run_stdio_async()
    finally:
        ros_node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
