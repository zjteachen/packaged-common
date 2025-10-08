"""ArducamIR implementation of the camera wrapper."""

import enum
from typing import Optional, Tuple, Literal

import cv2
import numpy as np
from numpy.typing import NDArray

import ArducamEvkSDK
import arducam_rgbir_remosaic

from . import base_camera

CAMERA_CONFIG_DIR = "./config/camera_config.cfg"


class ArducamOutput(enum.Enum):
    """
    Enum for ArducamIR output type.

    Attributes
    ----------
    RGB : int
        RGB image output.
    IR : int
        Infrared image output.
    """

    RGB = 0
    IR = 1


class CameraArducamIR(base_camera.BaseCameraDevice):
    """
    ArducamSDK implementation of the ArducamIR camera device.

    This class provides camera functionality using the ArducamEvkSDK library
    for Arducam RGB-IR camera modules.
    """

    __create_key = object()

    @classmethod
    def create(
        cls, width: int, height: int, config: None
    ) -> Tuple[Literal[True], "CameraArducamIR"] | Tuple[Literal[False], None]:
        """
        Create an ArducamIR camera instance.

        Parameters
        ----------
        width : int
            Width of the camera in pixels (unused for ArducamIR).
        height : int
            Height of the camera in pixels (unused for ArducamIR).
        config : None
            Configuration parameter (unused for ArducamIR).

        Returns
        -------
        tuple[Literal[True], CameraArducamIR] | tuple[Literal[False], None]
            Success status and camera object if successful, (False, None) otherwise.
        """
        camera = ArducamEvkSDK.Camera()

        param = ArducamEvkSDK.Param()
        param.config_file_name = CAMERA_CONFIG_DIR

        if not camera.open(param):
            return False, None

        return True, CameraArducamIR(cls.__create_key, camera)

    def __init__(
        self,
        class_private_create_key: object,
        camera: ArducamEvkSDK.Camera,
    ) -> None:
        """
        Private constructor, use create() method.

        Parameters
        ----------
        class_private_create_key : object
            Private key to prevent direct instantiation.
        camera : ArducamEvkSDK.Camera
            ArducamEvkSDK Camera object.
        """
        assert class_private_create_key is CameraArducamIR.__create_key, "Use create() method."

        self.__camera = camera
        self.__camera.init()
        self.__camera.start()

    def __del__(self) -> None:
        """
        Destructor. Release hardware resources.
        """
        self.__camera.stop()
        self.__camera.close()

    def run(self) -> Tuple[Literal[True], ArducamEvkSDK.Frame] | Tuple[Literal[False], None]:
        """
        Take a picture with ArducamIR camera.

        Returns
        -------
        tuple[Literal[True], ArducamEvkSDK.Frame] | tuple[Literal[False], None]
            Success status and raw Frame object if successful, (False, None) otherwise.
        """
        image_data = self.__camera.capture()
        if image_data is None:
            return False, None

        return True, image_data

    def demosaic(
        self, image: ArducamEvkSDK.Frame, output: ArducamOutput
    ) -> Optional[NDArray[np.uint8]]:
        """
        Convert Bayer Pattern and IR data to OpenCV matrix.

        This method processes the raw sensor data and converts it to either
        RGB or IR image format.

        Parameters
        ----------
        image : ArducamEvkSDK.Frame
            Raw frame from ArducamIR camera.
        output : ArducamOutput
            Desired output type (RGB or IR).

        Returns
        -------
        Optional[NDArray[np.uint8]]
            Processed image array in BGRA format, or None on failure.
        """
        # Convert sensor data to useable format
        data = self.format(image)
        # Splits raw sensor data into bayer data and IR data using GRIG (Green, Red, IR, Green) filter pattern
        bayer, ir = arducam_rgbir_remosaic.rgbir_remosaic(data, arducam_rgbir_remosaic.GRIG)
        if output == ArducamOutput.RGB:
            # Converts Bayer data to BGRA (Blue, Green, Red, Alpha)
            return cv2.cvtColor(bayer, cv2.COLOR_BayerRG2BGRA)
        # Converts IR data to BGRA
        ir_color = cv2.cvtColor(ir, cv2.COLOR_GRAY2BGRA)
        # Resize the IR image so that they are both the same size
        return cv2.resize(ir_color, (bayer.shape[1], bayer.shape[0]))

    def format(self, image: ArducamEvkSDK.Frame) -> NDArray[np.uint8]:
        """
        Format byte buffer sensor input into 8-bit arrays.

        This method converts the raw sensor data from the camera into a
        standardized 8-bit numpy array format.

        Parameters
        ----------
        image : ArducamEvkSDK.Frame
            Raw frame from ArducamIR camera.

        Returns
        -------
        NDArray[np.uint8]
            Formatted 8-bit image array with shape (height, width).
        """
        width = image.format.width
        height = image.format.height
        bit_depth = image.format.bit_depth
        data = image.data

        if bit_depth > 8:
            data = np.frombuffer(data, np.uint16).reshape(height, width)
            # Reduce higher precision inputs to 8-bit arrays
            data = (data >> (bit_depth - 8)).astype(np.uint8)
        else:
            data = np.frombuffer(data, np.uint8).reshape(height, width)

        return data
