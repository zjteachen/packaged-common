"""
3D position in WGS 84.

Class with name also available.
"""

from typing import Tuple, Literal, Optional


class PositionGlobal:
    """
    WGS 84 following ISO 6709 (latitude before longitude).
    """

    __create_key = object()

    @classmethod
    def create(
        cls, latitude: float, longitude: float, altitude: float
    ) -> Tuple[Literal[True], "PositionGlobal"]:
        """
        Create a PositionGlobal instance.

        Parameters
        ----------
        latitude : float
            Decimal degrees.
        longitude : float
            Decimal degrees.
        altitude : float
            Metres above mean sea level (MSL). Can be negative.

        Returns
        -------
        Tuple[Literal[True], PositionGlobal]
            Success status and the created PositionGlobal object.
        """
        return True, PositionGlobal(cls.__create_key, latitude, longitude, altitude)

    def __init__(
        self, class_private_create_key: object, latitude: float, longitude: float, altitude: float
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
        altitude : float
            Metres above mean sea level (MSL). Can be negative.
        """
        assert class_private_create_key is PositionGlobal.__create_key, "Use create() method."

        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

    def __str__(self) -> str:
        """
        Convert to string representation.

        Returns
        -------
        str
            String representation of the PositionGlobal object.
        """
        return f"{self.__class__}: latitude: {self.latitude}, longitude: {self.longitude}, altitude: {self.altitude}"

    def __repr__(self) -> str:
        """
        Representation for collections (e.g. list).

        Returns
        -------
        str
            String representation of the PositionGlobal object.
        """
        return str(self)


class NamedPositionGlobal(PositionGlobal):
    """
    Named PositionGlobal.
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
        altitude: float,
    ) -> Tuple[Literal[True], "NamedPositionGlobal"]:
        """
        Create a NamedPositionGlobal instance.

        Parameters
        ----------
        name : str
            Name for the position. Can be empty.
        latitude : float
            Decimal degrees.
        longitude : float
            Decimal degrees.
        altitude : float
            Metres above mean sea level (MSL). Can be negative.

        Returns
        -------
        Tuple[Literal[True], NamedPositionGlobal]
            Success status and the created NamedPositionGlobal object.
        """
        return True, NamedPositionGlobal(cls.__create_key, name, latitude, longitude, altitude)

    def __init__(
        self,
        class_private_create_key: object,
        name: str,
        latitude: float,
        longitude: float,
        altitude: float,
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
        altitude : float
            Metres above mean sea level (MSL). Can be negative.
        """
        assert class_private_create_key is NamedPositionGlobal.__create_key, "Use create() method."

        super().__init__(super()._PositionGlobal__create_key, latitude, longitude, altitude)

        self.name = name

    def __str__(self) -> str:
        """
        Convert to string representation.

        Returns
        -------
        str
            String representation of the NamedPositionGlobal object.
        """
        return f"{self.__class__}: name: {self.name}, latitude: {self.latitude}, longitude: {self.longitude}, altitude: {self.altitude}"
