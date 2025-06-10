#!/usr/bin/env python3

# Simple node to get the robot pose from the GPS sensor

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix
from parc_robot_bringup.gps2cartesian import gps_to_cartesian

class GetRobotPose(Node):
    def __init__(self):
        super().__init__("get_robot_pose")

        # Subscribe to the gps topic once
        self.gps_sub = self.create_subscription(NavSatFix, "/gps/fix", self.gps_callback, 1)

    def gps_callback(self, gps):

        # Get the cartesian coordinates from the GPS coordinates
        x, y = gps_to_cartesian(gps.latitude, gps.longitude)

        # Print cartesian coordinates
        self.get_logger().info("x: %.6f, y: %.6f" % (x, y))


def main(args=None):
    rclpy.init(args=args)

    get_robot_pose = GetRobotPose()
    rclpy.spin(get_robot_pose)

    get_robot_pose.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()