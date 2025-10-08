"""
Conversion between local and global space.
"""

from typing import Optional, Tuple

import pymap3d as pm

from . import drone_odometry_global
from . import drone_odometry_local
from .. import location_global
from .. import location_local
from .. import position_global
from .. import position_local


def position_global_from_position_local(
    home_position: position_global.PositionGlobal,
    local_position: position_local.PositionLocal,
) -> Tuple[bool, Optional[position_global.PositionGlobal]]:
    """
    Local coordinates to global coordinates.

    Parameters
    ----------
    home_position : position_global.PositionGlobal
        The home position in global coordinates.
    local_position : position_local.PositionLocal
        The local position to convert.

    Returns
    -------
    Tuple[bool, Optional[position_global.PositionGlobal]]
        A tuple containing success status and global position.
        Returns (False, None) if conversion fails.
    """
    latitude, longitude, altitude = pm.ned2geodetic(
        local_position.north,
        local_position.east,
        local_position.down,
        home_position.latitude,
        home_position.longitude,
        home_position.altitude,
    )

    result, global_position = position_global.PositionGlobal.create(
        latitude,
        longitude,
        altitude,
    )
    if not result:
        return False, None

    return True, global_position


def position_global_from_location_local(
    home_position: position_global.PositionGlobal,
    local_location: location_local.LocationLocal,
) -> Tuple[bool, Optional[position_global.PositionGlobal]]:
    """
    Local coordinates to global coordinates.

    Parameters
    ----------
    home_position : position_global.PositionGlobal
        The home position in global coordinates.
    local_location : location_local.LocationLocal
        The local location to convert.

    Returns
    -------
    Tuple[bool, Optional[position_global.PositionGlobal]]
        A tuple containing success status and global position.
        Returns (False, None) if conversion fails.
    """
    result, local_position = position_local.PositionLocal.create(
        local_location.north, local_location.east, 0.0
    )
    if not result:
        return False, None

    return position_global_from_position_local(home_position, local_position)


def position_local_from_position_global(
    home_position: position_global.PositionGlobal,
    global_position: position_global.PositionGlobal,
) -> Tuple[bool, Optional[position_local.PositionLocal]]:
    """
    Global coordinates to local coordinates.

    Parameters
    ----------
    home_position : position_global.PositionGlobal
        The home position in global coordinates.
    global_position : position_global.PositionGlobal
        The global position to convert.

    Returns
    -------
    Tuple[bool, Optional[position_local.PositionLocal]]
        A tuple containing success status and local position.
        Returns (False, None) if conversion fails.
    """
    north, east, down = pm.geodetic2ned(
        global_position.latitude,
        global_position.longitude,
        global_position.altitude,
        home_position.latitude,
        home_position.longitude,
        home_position.altitude,
    )

    result, local_position = position_local.PositionLocal.create(
        north,
        east,
        down,
    )
    if not result:
        return False, None

    return True, local_position


def position_local_from_location_global(
    home_position: position_global.PositionGlobal,
    global_location: location_global.LocationGlobal,
) -> Tuple[bool, Optional[position_local.PositionLocal]]:
    """
    Global coordinates to local coordinates.

    Parameters
    ----------
    home_position : position_global.PositionGlobal
        The home position in global coordinates.
    global_location : location_global.LocationGlobal
        The global location to convert.

    Returns
    -------
    Tuple[bool, Optional[position_local.PositionLocal]]
        A tuple containing success status and local position.
        Returns (False, None) if conversion fails.
    """
    result, global_position = position_global.PositionGlobal.create(
        global_location.latitude, global_location.longitude, home_position.altitude
    )
    if not result:
        return False, None

    return position_local_from_position_global(home_position, global_position)


def drone_odometry_local_from_global(
    home_position: position_global.PositionGlobal,
    odometry_global: drone_odometry_global.DroneOdometryGlobal,
) -> Tuple[bool, Optional[drone_odometry_local.DroneOdometryLocal]]:
    """
    Converts global odometry to local.

    Parameters
    ----------
    home_position : position_global.PositionGlobal
        The home position in global coordinates.
    odometry_global : drone_odometry_global.DroneOdometryGlobal
        The global odometry data to convert.

    Returns
    -------
    Tuple[bool, Optional[drone_odometry_local.DroneOdometryLocal]]
        A tuple containing success status and local odometry data.
        Returns (False, None) if conversion fails.
    """
    result, drone_position_local = position_local_from_position_global(
        home_position,
        odometry_global.position,
    )
    if not result:
        return False, None

    return drone_odometry_local.DroneOdometryLocal.create(
        drone_position_local,
        odometry_global.orientation,
    )
