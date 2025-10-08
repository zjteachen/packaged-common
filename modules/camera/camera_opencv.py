"""OpenCV implementation of the camera wrapper."""

from typing import Tuple, Literal

import cv2
import numpy as np
from numpy.typing import NDArray

from . import base_camera


class ConfigOpenCV:
    """
    Configuration for the OpenCV camera.

    Attributes
    ----------
    device_index : int
        Index of the camera device.
    """

    def __init__(self, device_index: int) -> None:
        """
        Initialize OpenCV camera configuration.

        Parameters
        ----------
        device_index : int
            Index of the camera device.
        """
        self.device_index = device_index


class CameraOpenCV(base_camera.BaseCameraDevice):
    """
    OpenCV implementation of the camera device.

    This class provides camera functionality using OpenCV's VideoCapture API.
    """

    __create_key = object()

    @classmethod
    def create(
        cls, width: int, height: int, config: ConfigOpenCV
    ) -> Tuple[Literal[True], "CameraOpenCV"] | Tuple[Literal[False], None]:
        """
        Create an OpenCV camera instance.

        Parameters
        ----------
        width : int
            Width of the camera in pixels.
        height : int
            Height of the camera in pixels.
        config : ConfigOpenCV
            Configuration for OpenCV camera.

        Returns
        -------
        tuple[Literal[True], CameraOpenCV] | tuple[Literal[False], None]
            Success status and camera object if successful, (False, None) otherwise.
        """
        if width <= 0:
            return False, None

        if height <= 0:
            return False, None

        camera = cv2.VideoCapture(config.device_index)
        if not camera.isOpened():
            return False, None

        camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        set_width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        set_height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        if set_width != width or set_height != height:
            return False, None

        return True, CameraOpenCV(cls.__create_key, camera)

    def __init__(self, class_private_create_key: object, camera: cv2.VideoCapture) -> None:
        """
        Private constructor, use create() method.

        Parameters
        ----------
        class_private_create_key : object
            Private key to prevent direct instantiation.
        camera : cv2.VideoCapture
            OpenCV VideoCapture object.
        """
        assert class_private_create_key is CameraOpenCV.__create_key, "Use create() method."

        self.__camera = camera

    def __del__(self) -> None:
        """
        Destructor. Release hardware resources.
        """
        self.__camera.release()

    def run(self) -> Tuple[Literal[True], NDArray[np.uint8]] | Tuple[Literal[False], None]:
        """
        Take a picture with OpenCV camera.

        Returns
        -------
        tuple[Literal[True], NDArray[np.uint8]] | tuple[Literal[False], None]
            Success status and image array with shape (height, width, channels in BGR)
            if successful, (False, None) otherwise.
        """
        result, image_data = self.__camera.read()
        if not result:
            return False, None

        return True, image_data
