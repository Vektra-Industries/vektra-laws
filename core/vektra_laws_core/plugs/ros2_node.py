"""ROS 2 node for the robot plug. Needs ROS 2 (rclpy); everything else in Vektra Laws Core does not.

Topics (remap to fit your robot):
  in   /vektra/cmd_vel/<source>   geometry_msgs/Twist   one per source: joystick, responder, nav, ai
  in   /vektra/person_distance    std_msgs/Float32      nearest person, meters (from your detector)
  in   /vektra/estop              std_msgs/Bool         true latches the stop (2.21)
  in   /vektra/stop_request       std_msgs/String       JSON {"id": "...", "role": "...", "danger": false}
  out  /cmd_vel                   geometry_msgs/Twist   the only publisher; fixed rate, zero when unsafe
  out  /vektra/status             std_msgs/String       the reason for the current command

Run:  ros2 run <your_pkg> vektra_motion_gate   (or python -m vektra_laws_core.plugs.ros2_node)
Keep the hardware emergency stop wired to the motor power. This node is not a safety-rated function.
"""
from __future__ import annotations

import json


def main() -> None:
    import rclpy
    from geometry_msgs.msg import Twist as RosTwist
    from rclpy.node import Node
    from std_msgs.msg import Bool, Float32, String

    from ..engine import Guard, Role, Speaker
    from .robot import DEFAULT_SOURCES, Limits, MotionGate, Twist

    class GateNode(Node):
        def __init__(self):
            super().__init__("vektra_motion_gate")
            lim = Limits(**{k: self.declare_parameter(k, v).value
                            for k, v in Limits().__dict__.items()})
            rate = self.declare_parameter("rate_hz", 20.0).value
            self.gate = MotionGate(Guard(), lim)
            self.pub = self.create_publisher(RosTwist, "/cmd_vel", 10)
            self.status = self.create_publisher(String, "/vektra/status", 10)
            for name, _, _ in DEFAULT_SOURCES:
                self.create_subscription(RosTwist, f"/vektra/cmd_vel/{name}",
                                         lambda m, n=name: self.gate.submit(
                                             n, Twist(m.linear.x, m.angular.z), self.now()), 10)
            self.create_subscription(Float32, "/vektra/person_distance",
                                     lambda m: self.gate.person_distance(m.data, self.now()), 10)
            self.create_subscription(Bool, "/vektra/estop",
                                     lambda m: m.data and self.gate.estop("estop topic"), 10)
            self.create_subscription(String, "/vektra/stop_request", self.on_stop, 10)
            self.create_timer(1.0 / rate, self.tick)

        def now(self) -> float:
            return self.get_clock().now().nanoseconds / 1e9

        def on_stop(self, m):
            d = json.loads(m.data)
            self.gate.stop_request(Speaker(d.get("id", ""), Role(d.get("role", "other_person"))),
                                   bool(d.get("danger")))

        def tick(self):
            c = self.gate.tick(self.now())
            out = RosTwist()
            out.linear.x, out.angular.z = c.linear, c.angular
            self.pub.publish(out)
            self.status.publish(String(data=self.gate.last_reason))

    rclpy.init()
    node = GateNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
