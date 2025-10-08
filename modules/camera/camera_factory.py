"""Factory pattern for constructing camera device class at runtime."""

import enum
from typing import Union, Tuple, Literal

from . import base_camera
from . import camera_opencv
from . import camera_picamera2
from . import camera_arducamir


class CameraOption(enum.Enum):
    """
    Enumeration for type of camera object to create.

    Attributes
    ----------
    OPENCV : int
        OpenCV camera implementation.
    PICAM2 : int
        Picamera2 camera implementation (Raspberry Pi).
    ARDUCAMIR : int
        ArducamIR camera implementation.
    """

    OPENCV = 0
    PICAM2 = 1
    ARDUCAMIR = 2


def create_camera(
    camera_option: CameraOption,
    width: int,
    height: int,
    config: Union[camera_opencv.ConfigOpenCV, camera_picamera2.ConfigPiCamera2, None],
) -> Tuple[Literal[True], base_camera.BaseCameraDevice] | Tuple[Literal[False], None]:
    """
    Create a camera object based on given parameters.

    This factory function creates the appropriate camera device implementation
    based on the specified camera option.

    Parameters
    ----------
    camera_option : CameraOption
        Type of camera to create (OPENCV, PICAM2, or ARDUCAMIR).
    width : int
        Width of the camera in pixels.
    height : int
        Height of the camera in pixels.
    config : Union[ConfigOpenCV, ConfigPiCamera2, None]
        Configuration object for the selected camera type.

    Returns
    -------
    tuple[Literal[True], BaseCameraDevice] | tuple[Literal[False], None]
        Success status and camera device object if successful, (False, None) otherwise.
    """
    match camera_option:
        case CameraOption.OPENCV:
            return camera_opencv.CameraOpenCV.create(width, height, config)
        case CameraOption.PICAM2:
            return camera_picamera2.CameraPiCamera2.create(width, height, config)
        case CameraOption.ARDUCAMIR:
            return camera_arducamir.CameraArducamIR.create(width, height, config)

    return False, None
