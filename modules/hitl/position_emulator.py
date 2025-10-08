"""
Emulates position and attitude to Pixhawk.
"""

import time
from typing import Tuple
from ..mavlink import dronekit


class PositionEmulator:
    """
    Setup for position emulator.
    """

    __create_key = object()

    @classmethod
    def create(
        cls, drone: dronekit.Vehicle
    ) -> Tuple[bool, "PositionEmulator"]:
        """
        Set up position emulator.

        Parameters
        ----------
        drone : dronekit.Vehicle
            The dronekit instance to use for sending MAVLink messages.

        Returns
        -------
        Tuple[bool, PositionEmulator]
            A tuple containing success status and PositionEmulator instance.
        """

        return True, PositionEmulator(cls.__create_key, drone)

    def __init__(self, class_private_create_key: object, drone: dronekit.Vehicle) -> None:
        """
        Private constructor, use create() method.

        Parameters
        ----------
        class_private_create_key : object
            Private key to ensure constructor is only called via create().
        drone : dronekit.Vehicle
            The dronekit instance to use for sending MAVLink messages.
        """
        assert class_private_create_key is PositionEmulator.__create_key, "Use create() method"

        self.target_position = (43.43405014107003, -80.57898027451816, 373.0)  # lat, lon, alt

        self.drone = drone

    def set_target_position(self, latitude: float, longitude: float, altitude: float) -> None:
        """
        Set the target position manually.

        This is currently a fallback if Ardupilot target doesn't work.

        Parameters
        ----------
        latitude : float
            Latitude in degrees.
        longitude : float
            Longitude in degrees.
        altitude : float
            Altitude in meters.
        """
        self.target_position = (latitude, longitude, altitude)

    def get_target_position(self) -> Tuple[float, float, float]:
        """
        Get the target position from the Ardupilot target.

        Returns
        -------
        Tuple[float, float, float]
            Target position as (latitude, longitude, altitude) in degrees and meters.
        """
        # pylint: disable=protected-access
        position_target = None
        try:
            position_target = self.drone._master.recv_match(
                type="POSITION_TARGET_GLOBAL_INT", blocking=False
            )
        except Exception as exc:  # pylint: disable=broad-except
            print(f"HITL get_target_position recv_match error: {exc}")
            position_target = None
        # pylint: enable=protected-access

        if position_target:
            latitude = position_target.lat_int / 1e7
            longitude = position_target.lon_int / 1e7
            altitude = position_target.alt
            return (latitude, longitude, altitude)

        # Optionally log if no message received
        # print("No POSITION_TARGET_GLOBAL_INT message received.")

        return self.target_position

    def periodic(self) -> None:
        """
        Execute periodic position emulation tasks.

        Updates the target position from Ardupilot and injects the current
        position into the flight controller.
        """

        self.target_position = self.get_target_position()

        self.inject_position(
            self.target_position[0], self.target_position[1], self.target_position[2]
        )

    def inject_position(
        self,
        latitude: float = 43.43405014107003,
        longitude: float = -80.57898027451816,
        altitude: float = 373.0,
    ) -> None:
        """
        Simulate GPS coordinates by injecting the desired position of the drone.

        Parameters
        ----------
        latitude : float, optional
            Latitude in degrees, by default 43.43405014107003.
        longitude : float, optional
            Longitude in degrees, by default -80.57898027451816.
        altitude : float, optional
            Altitude in meters, by default 373.0.
        """
        values = [
            int(time.time() * 1e6),  # time_usec
            0,  # gps_id
            0b111111,  # ignore_flags (all fields valid)
            0,  # time_week_ms
            0,  # time_week
            3,  # fix_type (3D fix)
            int(latitude * 1e7),  # lat
            int(longitude * 1e7),  # lon
            int(altitude * 1000),  # alt (mm)
            100,  # hdop (x100)
            100,  # vdop (x100)
            0,  # vn (cm/s)
            0,  # ve (cm/s)
            0,  # vd (cm/s)
            100,  # speed_accuracy (cm/s)
            100,  # horiz_accuracy (cm)
            100,  # vert_accuracy (cm)
            10,  # satellites_visible
            0,  # yaw (deg*100)
        ]
        gps_input_msg = self.drone.message_factory.gps_input_encode(*values)
        self.drone.send_mavlink(gps_input_msg)
        self.drone.flush()
