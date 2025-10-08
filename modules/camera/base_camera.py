"""Base class for camera device."""

import abc
from typing import Optional, Tuple, Literal

import numpy as np
from numpy.typing import NDArray


class BaseCameraDevice(abc.ABC):
    """
    Abstract class for camera device implementations.

    This class provides an interface for camera devices that can capture images.
    """

    @classmethod
    @abc.abstractmethod
    def create(
        cls,
        width: int,
        height: int,
        config: object,
    ) -> Tuple[Literal[True], "BaseCameraDevice"] | Tuple[Literal[False], None]:
        """
        Abstract create method.

        Parameters
        ----------
        width : int
            Width of the camera in pixels.
        height : int
            Height of the camera in pixels.
        config : object
            Configuration object for the camera.

        Returns
        -------
        tuple[Literal[True], BaseCameraDevice] | tuple[Literal[False], None]
            Success status and camera object if successful, (False, None) otherwise.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def __init__(self, class_private_create_key: object, camera: object) -> None:
        """
        Abstract private constructor.

        Parameters
        ----------
        class_private_create_key : object
            Private key to prevent direct instantiation.
        camera : object
            Camera device object.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def __del__(self) -> None:
        """
        Destructor. Release hardware resources.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def run(self) -> Tuple[Literal[True], NDArray[np.uint8]] | Tuple[Literal[False], None]:
        """
        Take a picture with camera device.

        Returns
        -------
        tuple[Literal[True], NDArray[np.uint8]] | tuple[Literal[False], None]
            Success status and image array with shape (height, width, channels in BGR)
            if successful, (False, None) otherwise.
        """
        raise NotImplementedError
