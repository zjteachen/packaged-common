"""Picamera2 implementation of the camera wrapper."""

from typing import Optional, Tuple, Literal, Dict, Union

import numpy as np
from numpy.typing import NDArray

# Picamera2 library only exists on Raspberry Pi
try:
    import libcamera
    import picamera2
except ImportError:
    picamera2 = None

from . import base_camera


class ConfigPiCamera2:
    """
    Configuration for the PiCamera.

    Attributes
    ----------
    timeout : float
        Getting image timeout in seconds.
    exposure_time : int
        Exposure time in microseconds.
    analogue_gain : float
        Analogue gain value (0.0 to 64.0). ISO = Analogue gain * Digital gain * 100.
    contrast : float
        Contrast value (0.0 to 32.0). 0.0 is no contrast, 1.0 is normal contrast, higher is more contrast.
    maybe_lens_position : Optional[float]
        Position of the lens in dioptres (reciprocal of metres: 1/m). 0 means infinite distance.
    """

    def __init__(
        self,
        timeout: float = 1.0,
        exposure_time: int = 250,
        analogue_gain: float = 64.0,
        contrast: float = 1.0,
        maybe_lens_position: Optional[float] = None,
    ) -> None:
        """
        Initialize PiCamera2 configuration.

        Parameters
        ----------
        timeout : float, optional
            Getting image timeout in seconds. Default is 1.0.
        exposure_time : int, optional
            Exposure time in microseconds. Default is 250.
        analogue_gain : float, optional
            Analogue gain value (0.0 to 64.0). ISO = Analogue gain * Digital gain * 100. Default is 64.0.
        contrast : float, optional
            Contrast value (0.0 to 32.0). 0.0 is no contrast, 1.0 is normal contrast, higher is more contrast. Default is 1.0.
        maybe_lens_position : Optional[float], optional
            Position of the lens in dioptres (reciprocal of metres: 1/m). 0 means infinite distance. Default is None.
        """
        self.timeout = timeout

        self.exposure_time = exposure_time
        self.analogue_gain = analogue_gain
        self.contrast = contrast
        self.maybe_lens_position = maybe_lens_position

    def to_dict(self) -> Dict[str, Union[int, float, object]]:
        """
        Create dictionary containing camera controls.

        Returns
        -------
        Dict[str, Union[int, float, object]]
            Dictionary containing camera control parameters.
        """
        camera_controls: Dict[str, Union[int, float, object]] = {
            "ExposureTime": self.exposure_time,
            "AnalogueGain": self.analogue_gain,
            "Contrast": self.contrast,
        }

        if self.maybe_lens_position is not None:
            camera_controls["LensPosition"] = self.maybe_lens_position
            camera_controls["AfMode"] = libcamera.controls.AfModeEnum.Manual
        else:
            camera_controls["LensPosition"] = 0.0
            camera_controls["AfMode"] = libcamera.controls.AfModeEnum.Auto

        return camera_controls


if picamera2 is None:

    class CameraPiCamera2(base_camera.BaseCameraDevice):
        """
        Placeholder class for Picamera2 when library is not available.

        This class is used when the picamera2 library cannot be imported,
        typically on non-Raspberry Pi systems.
        """

        @classmethod
        def create(
            cls, width: int, height: int, config: ConfigPiCamera2
        ) -> Tuple[Literal[False], None]:
            """
            Create method that always fails when picamera2 is not available.

            Parameters
            ----------
            width : int
                Width of the camera in pixels.
            height : int
                Height of the camera in pixels.
            config : ConfigPiCamera2
                Configuration for PiCamera2 camera.

            Returns
            -------
            tuple[Literal[False], None]
                Always returns (False, None) since picamera2 is not available.
            """
            return False, None

        def __init__(self) -> None:
            """
            Initialize placeholder camera object.
            """
            pass

else:

    class CameraPiCamera2(base_camera.BaseCameraDevice):
        """
        Picamera2 implementation of the camera device.

        This class provides camera functionality using the Picamera2 library
        for Raspberry Pi camera modules.
        """

        __create_key = object()

        @classmethod
        def create(
            cls, width: int, height: int, config: ConfigPiCamera2
        ) -> Tuple[Literal[True], "CameraPiCamera2"] | Tuple[Literal[False], None]:
            """
            Create a Picamera2 camera instance.

            Parameters
            ----------
            width : int
                Width of the camera in pixels.
            height : int
                Height of the camera in pixels.
            config : ConfigPiCamera2
                Configuration for PiCamera2 camera.

            Returns
            -------
            tuple[Literal[True], CameraPiCamera2] | tuple[Literal[False], None]
                Success status and camera object if successful, (False, None) otherwise.
            """
            if width <= 0:
                return False, None

            if height <= 0:
                return False, None

            try:
                camera = picamera2.Picamera2()

                camera_config = camera.create_preview_configuration(
                    {"size": (width, height), "format": "RGB888"}
                )
                camera.configure(camera_config)
                camera.start()
                controls = config.to_dict()
                camera.set_controls(controls)

                return True, CameraPiCamera2(cls.__create_key, camera, config)
            except RuntimeError:
                return False, None

        def __init__(
            self,
            class_private_create_key: object,
            camera: picamera2.Picamera2,  # type: ignore
            config: ConfigPiCamera2,
        ) -> None:
            """
            Private constructor, use create() method.

            Parameters
            ----------
            class_private_create_key : object
                Private key to prevent direct instantiation.
            camera : picamera2.Picamera2
                Picamera2 camera object.
            config : ConfigPiCamera2
                Configuration for PiCamera2 camera.
            """
            assert class_private_create_key is CameraPiCamera2.__create_key, "Use create() method."

            self.__camera = camera
            self.__config = config

        def __del__(self) -> None:
            """
            Destructor. Release hardware resources.
            """
            self.__camera.close()

        def run(self) -> Tuple[Literal[True], NDArray[np.uint8]] | Tuple[Literal[False], None]:
            """
            Take a picture with Picamera2 camera.

            Returns
            -------
            tuple[Literal[True], NDArray[np.uint8]] | tuple[Literal[False], None]
                Success status and image array with shape (height, width, channels in RGB)
                if successful, (False, None) otherwise.
            """
            try:
                image_data = self.__camera.capture_array(wait=self.__config.timeout)
            except TimeoutError:
                return False, None

            return True, image_data
