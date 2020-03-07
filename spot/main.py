import logging
import time

from bosdyn.api.robot_state_pb2 import RobotState
import bosdyn.client.util
from spot.config import read_config
from spot import __version__

from spot.robot import RobotStates, RobotConnection
from spot.vision import RobotVision

logger = logging.getLogger(__name__)


def main():
    config: Config = read_config("config.yaml")

    try:
        connection = RobotConnection(config.spot)
    except:
        logger.exception("Robot connection failed")
        time.sleep(1)

    while True:
        try:
            pass
            #robot = RobotStates(connection)
            #robot.extract_joints(robot.get_states_cb)
            #robot.extract_kinematic_odometry(robot.get_states_cb)

            vision = RobotVision(connection)
            vision.get_image()
        except Exception as exc:
            logger = bosdyn.client.util.get_logger()
            logger.error("Spot threw an exception: %s", exc)
            return False
