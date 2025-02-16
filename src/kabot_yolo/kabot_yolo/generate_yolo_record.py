import rclpy
from rclpy.node import Node

from kabot_msgs.srv import CaptureRobotImage

from geometry_msgs.msg import Pose
from sensor_msgs.msg import Image

from functools import partial

class CaptureRobotImageService(Node):
    def __init__(self):
        super().__init__('capture_robot_image_service')

        self.latest_image = None
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.camera_callback,
            10
        )

        self.srv = self.create_service(
            CaptureRobotImage,
            'capture_robot_image',
            self.handle_capture_robot_image
        )

    def camera_callback(self, msg):
        self.latest_image = msg

    def handle_capture_robot_image(self, request, response):

        if not self.spawn_robot_in_gazebo(request.robot_pose):
            self.get_logger().error("KabotSpawn error")
            return response


        rclpy.spin_once(self, timeout_sec=1.0)
        if self.latest_image is None:
            self.get_logger().warn("No image error")
            return response

        response.image = self.latest_image

        return response

    def spawn_robot_in_gazebo(self, pose: Pose) -> bool:
        return True

def main(args=None):
    rclpy.init(args=args)

    node = CaptureRobotImageService()
    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == '__main__':
    main()
