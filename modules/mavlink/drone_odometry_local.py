"""
Drone odometry in local space (origin at home position global).
"""

from typing import Optional, Tuple

from .. import orientation
from .. import position_local


class DroneOdometryLocal:
    """
    Wrapper for position and orientation.
    """

    __create_key = object()

    @classmethod
    def create(
        cls,
        drone_position: position_local.PositionLocal,
        drone_orientation: orientation.Orientation,
    ) -> Tuple[bool, Optional["DroneOdometryLocal"]]:
        """
        Position and orientation in one class.

        Parameters
        ----------
        drone_position : position_local.PositionLocal
            The drone's local position.
        drone_orientation : orientation.Orientation
            The drone's orientation.

        Returns
        -------
        Tuple[bool, Optional[DroneOdometryLocal]]
            A tuple containing success status and DroneOdometryLocal instance.
            Returns (False, None) if any parameter is None.
        """
        if drone_position is None:
            return False, None

        if drone_orientation is None:
            return False, None

        return True, DroneOdometryLocal(cls.__create_key, drone_position, drone_orientation)

    def __init__(
        self,
        class_private_create_key: object,
        drone_position: position_local.PositionLocal,
        drone_orientation: orientation.Orientation,
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is DroneOdometryLocal.__create_key, "Use create() method."

        self.position = drone_position
        self.orientation = drone_orientation

    def __str__(self) -> str:
        """
        To string.
        """
        return f"{self.__class__}: Position: {self.position}, orientation: {self.orientation}"

    def __repr__(self) -> str:
        """
        For collections (e.g. list).
        """
        return str(self)
