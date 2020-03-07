import sys
import time

import bosdyn.client
import bosdyn.client.estop
import bosdyn.client.lease
import bosdyn.client.util
import bosdyn.geometry

from spot.robot import RobotConnection
from bosdyn.client.robot_command import RobotCommandBuilder, RobotCommandClient, blocking_stand

# command
from bosdyn.api import geometry_pb2, trajectory_pb2
from bosdyn.api.spot import robot_command_pb2 as spot_command_pb2


class RobotCommand:
    def __init__(self, connection: RobotConnection):

        self.robot = connection.robot
        self.robot.time_sync.wait_for_sync()
        estop_client = self.robot.ensure_client(bosdyn.client.estop.EstopClient.default_service_name)
        estop_endpoint = bosdyn.client.estop.EstopEndpoint(client=estop_client, name='HelloSpot', estop_timeout=9.0)
        estop_endpoint.force_simple_setup()
        lease_client = self.robot.ensure_client(bosdyn.client.lease.LeaseClient.default_service_name)
        lease = lease_client.acquire()

        bosdyn.client.util.setup_logging(verbose=False)

        try:
            with bosdyn.client.lease.LeaseKeepAlive(lease_client), bosdyn.client.estop.EstopKeepAlive(estop_endpoint):
                self.robot.logger.info("Powering on robot... This may take a few seconds")
                self.robot.power_on(timeout_sec=20)
                assert self.robot.is_powered_on(), "Robot power on failed"
                self.robot.logger.info("Robot is powered on")
                self.move_around()
        finally:
            lease_client.return_lease(lease)

    def move_around(self):
        command_client = self.robot.ensure_client(RobotCommandClient.default_service_name)
        blocking_stand(command_client, timeout_sec=10)
        self.robot.logger.info("Robot standing tall")
        time.sleep(3)
        frame_name = geometry_pb2.Frame(base_frame=geometry_pb2.FRAME_KO)
        cmd = RobotCommandBuilder.trajectory_command(goal_x=1.0, goal_y=1.0, goal_heading=0.0,
                                                     frame=frame_name, params=None,
                                                     locomotion_hint=spot_command_pb2.HINT_AUTO)

        end_time = 2.0
        command_client.robot_command(lease=None, command=cmd, end_time_secs=time.time() + end_time)
        start_time = time.time()
        current_time = time.time()
        while current_time - start_time < end_time:
            time.sleep(0.25)
            current_time = time.time()
        return True
