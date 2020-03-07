"""
Spot Mini access.
"""

import logging
import time

import bosdyn.client
import bosdyn.client.util
from bosdyn.client.image import ImageClient
from bosdyn.client.robot_state import RobotStateClient
from bosdyn.api.robot_state_pb2 import KinematicState, RobotState, RobotMetrics, JointState
import os

from spot.config import SpotConfig, Config

logger = logging.getLogger(__name__)


class RobotConnection:
    def __init__(self, spot: SpotConfig):
        logger.info("app token %s", spot.app_token)
        self.sdk = bosdyn.client.create_standard_sdk('SpotExtractor')
        self.sdk.load_app_token(spot.app_token)
        self.robot = self.sdk.create_robot(spot.hostname)
        self.robot.authenticate(spot.username, spot.password)
        self.robot_state_client = self.robot.ensure_client(RobotStateClient.default_service_name)
        self.image_client = self.robot.ensure_client(ImageClient.default_service_name)


class RobotStates:
    def __init__(self, connection: RobotConnection):
        self.connection = connection

        self.x = 0
        self.y = 0
        self.z = 0

        self.qx = 0
        self.qy = 0
        self.qz = 0
        self.qw = 1

    def get_states_cb(self):
        self.state = self.connection.robot_state_client.get_robot_state()
        time.sleep(0.05)
        print(self.state)

    def extract_joints(self, callback=None):
        callback()
        joints = self.state.kinematic_state.joint_states
        # print("-----------------------------------------")
        names = [js.name for js in joints]
        positions = [js.position.value for js in joints]
        velocities = [js.velocity.value for js in joints]

        #print(names)

    def extract_kinematic_odometry(self, callback=None):
        callback()
        odom = self.state.kinematic_state.vo_tform_body
        self.x = odom.position.x
        self.y = odom.position.y
        self.z = odom.position.z
        self.qx = odom.rotation.x
        self.qy = odom.rotation.y
        self.qz = odom.rotation.z
        self.qw = odom.rotation.w