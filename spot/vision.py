from spot.robot import RobotConnection
from bosdyn.client.image import ImageClient, build_image_request
from bosdyn.api import image_pb2
import bosdyn.client

import time
import cv2
import numpy as np
from PIL import Image
import io

class RobotVision:

    def __init__(self, connection: RobotConnection):
        self.connection = connection
        self.image_request_frontleft = build_image_request(image_source_name="frontleft_fisheye_image",
                                                           quality_percent=75,
                                                           image_format=image_pb2.Image.FORMAT_UNKNOWN)

        self.image_request_frontright = build_image_request(image_source_name="frontright_fisheye_image",
                                                            quality_percent=75,
                                                            image_format=image_pb2.Image.FORMAT_UNKNOWN)
        self.image_requests = [self.image_request_frontleft, self.image_request_frontright]

    def get_image_from_bytes(self):
        image_response = self.connection.image_client.get_image_from_sources(["left_fisheye_image"])[0]
        image = Image.open(io.BytesIO(image_response.shot.image.data))
        image.show()

    def get_image(self):
        image_responses = self.connection.image_client.get_image(self.image_requests)
        for image in image_responses:
            if image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_DEPTH_U16:
                dtype = np.uint16
            else:
                dtype = np.uint8
            img = np.fromstring(image.shot.image.data, dtype=dtype)
            if image.shot.image.format == image_pb2.Image.FORMAT_RAW:
                img = img.reshape(image.shot.image.rows, image.shot.image.cols)
            else:
                img = cv2.imdecode(img, -1)
            cv2.imshow(image.source.name, img)
        cv2.waitKey(1)
