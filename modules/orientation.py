"""
Orientation of object in 3D space.
"""

import math
from typing import Tuple, Literal, Optional


class Orientation:
    """
    Yaw, pitch, roll following NED system (x forward, y right, z down).
    Specifically, intrinsic (Tait-Bryan) rotations in the zyx/3-2-1 order.

    Orientation is identical in local and global space.
    """

    __create_key = object()

    @classmethod
    def create(
        cls,
        yaw: float,
        pitch: float,
        roll: float,
    ) -> Tuple[Literal[True], "Orientation"] | Tuple[Literal[False], None]:
        """
        Create an Orientation instance.

        Parameters
        ----------
        yaw : float
            Radians of [-pi, pi].
        pitch : float
            Radians of [-pi, pi].
        roll : float
            Radians of [-pi, pi].

        Returns
        -------
        Tuple[Literal[True], Orientation] | Tuple[Literal[False], None]
            Success status and the created Orientation object if successful,
            or False and None if parameters are out of range.
        """
        if yaw < -math.pi or yaw > math.pi:
            return False, None

        if pitch < -math.pi or pitch > math.pi:
            return False, None

        if roll < -math.pi or roll > math.pi:
            return False, None

        return True, Orientation(cls.__create_key, yaw, pitch, roll)

    def __init__(
        self, class_private_create_key: object, yaw: float, pitch: float, roll: float
    ) -> None:
        """
        Private constructor, use create() method.

        Parameters
        ----------
        class_private_create_key : object
            Private key to prevent direct instantiation.
        yaw : float
            Radians of [-pi, pi].
        pitch : float
            Radians of [-pi, pi].
        roll : float
            Radians of [-pi, pi].
        """
        assert class_private_create_key is Orientation.__create_key, "Use create() method."

        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll

    def __str__(self) -> str:
        """
        Convert to string representation.

        Returns
        -------
        str
            String representation of the Orientation object.
        """
        return f"{self.__class__} YPR radians: {self.yaw}, {self.pitch}, {self.roll}"

    def __repr__(self) -> str:
        """
        Representation for collections (e.g. list).

        Returns
        -------
        str
            String representation of the Orientation object.
        """
        return str(self)
