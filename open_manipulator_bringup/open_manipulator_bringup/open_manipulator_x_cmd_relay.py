#!/usr/bin/env python3
"""Relay output from a joint_state_topic_interface controller to individual commands

Subscriptions
- sensor_msgs.msg.JointState on /robot_joint_commands

Publications
- std_msgs.msg.Float64 on /{joint_name}/cmd_pos
- std_msgs.msg.Float64 on /{joint_name}/cmd_vel

Usage

Launch Gazebo and controllers
-

Launch command relay
-

Send command
-

Inspect command
-

"""

import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64

JOINT_TOPICS = {
    "joint1": "/joint1/cmd_pos",
    "joint2": "/joint2/cmd_pos",
    "joint3": "/joint3/cmd_pos",
    "joint4": "/joint4/cmd_pos",
    "gripper_left_joint": "/gripper_left_joint/cmd_pos",
}


class AckermannJointCommands(Node):
    def __init__(self):
        super().__init__("open_manipulator_x_joint_relay")
        self.pubs = {}
        for joint_name, topic in JOINT_TOPICS.items():
            self.pubs[joint_name] = self.create_publisher(Float64, topic, 10)
        self.create_subscription(
            JointState, "/robot_joint_commands", self.on_joint_command, 10
        )

    def on_joint_command(self, msg):
        for i, name in enumerate(msg.name):
            if name in self.pubs:
                cmd = Float64()
                if not math.isnan(msg.position[i]):
                    # position command
                    cmd.data = msg.position[i]
                elif not math.isnan(msg.velocity[i]):
                    # velocity command
                    cmd.data = msg.velocity[i]
                self.pubs[name].publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = AckermannJointCommands()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
