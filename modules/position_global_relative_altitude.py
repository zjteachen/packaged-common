"""
3D position in WGS 84.

Class with name also available.
"""

from typing import Tuple, Literal, Optional


class PositionGlobalRelativeAltitude:
    """
    WGS 84 following ISO 6709 (latitude before longitude).

    Relative altitude to home position.
    """

    __create_key = object()

    @classmethod
    def create(
        cls, latitude: float, longitude: float, relative_altitude: float
    ) -> Tuple[Literal[True], "PositionGlobalRelativeAltitude"]:
        """
        Create a PositionGlobalRelativeAltitude instance.

        Parameters
        ----------
        latitude : float
            Decimal degrees.
        longitude : float
            Decimal degrees.
        relative_altitude : float
            Metres above home position. Can be negative.

        Returns
        -------
        Tuple[Literal[True], PositionGlobalRelativeAltitude]
            Success status and the created PositionGlobalRelativeAltitude object.
        """
        return True, PositionGlobalRelativeAltitude(
            cls.__create_key, latitude, longitude, relative_altitude
        )

    def __init__(
        self,
        class_private_create_key: object,
        latitude: float,
        longitude: float,
        relative_altitude: float,
    ) -> None:
        """
        Private constructor, use create() method.

        Parameters
        ----------
        class_private_create_key : object
            Private key to prevent direct instantiation.
        latitude : float
            Decimal degrees.
        longitude : float
            Decimal degrees.
        relative_altitude : float
            Metres above home position. Can be negative.
        """
        assert (
            class_private_create_key is PositionGlobalRelativeAltitude.__create_key
        ), "Use create() method."

        self.latitude = latitude
        self.longitude = longitude
        self.relative_altitude = relative_altitude

    def __str__(self) -> str:
        """
        Convert to string representation.

        Returns
        -------
        str
            String representation of the PositionGlobalRelativeAltitude object.
        """
        return f"{self.__class__}: latitude: {self.latitude}, longitude: {self.longitude}, relative altitude: {self.relative_altitude}"

    def __repr__(self) -> str:
        """
        Representation for collections (e.g. list).

        Returns
        -------
        str
            String representation of the PositionGlobalRelativeAltitude object.
        """
        return str(self)


class NamedPositionGlobalRelativeAltitude(PositionGlobalRelativeAltitude):
    """
    Named PositionGlobalRelativeAltitude.
    """

    __create_key = object()

    @classmethod
    # Additional argument for name
    # pylint: disable-next=arguments-differ
    def create(
        cls,
        name: str,
        latitude: float,
        longitude: float,
        relative_altitude: float,
    ) -> Tuple[Literal[True], "NamedPositionGlobalRelativeAltitude"]:
        """
        Create a NamedPositionGlobalRelativeAltitude instance.

        Parameters
        ----------
        name : str
            Name for the position. Can be empty.
        latitude : float
            Decimal degrees.
        longitude : float
            Decimal degrees.
        relative_altitude : float
            Metres above home position. Can be negative.

        Returns
        -------
        Tuple[Literal[True], NamedPositionGlobalRelativeAltitude]
            Success status and the created NamedPositionGlobalRelativeAltitude object.
        """
        return True, NamedPositionGlobalRelativeAltitude(
            cls.__create_key, name, latitude, longitude, relative_altitude
        )

    def __init__(
        self,
        class_private_create_key: object,
        name: str,
        latitude: float,
        longitude: float,
        relative_altitude: float,
    ) -> None:
        """
        Private constructor, use create() method.

        Parameters
        ----------
        class_private_create_key : object
            Private key to prevent direct instantiation.
        name : str
            Name for the position.
        latitude : float
            Decimal degrees.
        longitude : float
            Decimal degrees.
        relative_altitude : float
            Metres above home position. Can be negative.
        """
        assert (
            class_private_create_key is NamedPositionGlobalRelativeAltitude.__create_key
        ), "Use create() method."

        super().__init__(
            super()._PositionGlobalRelativeAltitude__create_key,
            latitude,
            longitude,
            relative_altitude,
        )

        self.name = name

    def __str__(self) -> str:
        """
        Convert to string representation.

        Returns
        -------
        str
            String representation of the NamedPositionGlobalRelativeAltitude object.
        """
        return f"{self.__class__}: name: {self.name}, latitude: {self.latitude}, longitude: {self.longitude}, relative_altitude: {self.relative_altitude}"
