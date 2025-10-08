"""
Location on ground in WGS 84.

Class with name also available.
"""

from typing import Tuple, Literal, Optional


class LocationGlobal:
    """
    WGS 84 following ISO 6709 (latitude before longitude).
    """

    __create_key = object()

    @classmethod
    def create(
        cls, latitude: float, longitude: float
    ) -> Tuple[Literal[True], "LocationGlobal"]:
        """
        Create a LocationGlobal instance.

        Parameters
        ----------
        latitude : float
            Decimal degrees.
        longitude : float
            Decimal degrees.

        Returns
        -------
        Tuple[Literal[True], LocationGlobal]
            Success status and the created LocationGlobal object.
        """
        return True, LocationGlobal(cls.__create_key, latitude, longitude)

    def __init__(self, class_private_create_key: object, latitude: float, longitude: float) -> None:
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
        """
        assert class_private_create_key is LocationGlobal.__create_key, "Use create() method."

        self.latitude = latitude
        self.longitude = longitude

    def __str__(self) -> str:
        """
        Convert to string representation.

        Returns
        -------
        str
            String representation of the LocationGlobal object.
        """
        return f"{self.__class__}: latitude: {self.latitude}, longitude: {self.longitude}"

    def __repr__(self) -> str:
        """
        Representation for collections (e.g. list).

        Returns
        -------
        str
            String representation of the LocationGlobal object.
        """
        return str(self)


class NamedLocationGlobal(LocationGlobal):
    """
    Named LocationGlobal.
    """

    __create_key = object()

    @classmethod
    # Additional argument for name
    # pylint: disable-next=arguments-differ
    def create(
        cls, name: str, latitude: float, longitude: float
    ) -> Tuple[Literal[True], "NamedLocationGlobal"]:
        """
        Create a NamedLocationGlobal instance.

        Parameters
        ----------
        name : str
            Name for the location. Can be empty.
        latitude : float
            Decimal degrees.
        longitude : float
            Decimal degrees.

        Returns
        -------
        Tuple[Literal[True], NamedLocationGlobal]
            Success status and the created NamedLocationGlobal object.
        """
        return True, NamedLocationGlobal(cls.__create_key, name, latitude, longitude)

    def __init__(
        self, class_private_create_key: object, name: str, latitude: float, longitude: float
    ) -> None:
        """
        Private constructor, use create() method.

        Parameters
        ----------
        class_private_create_key : object
            Private key to prevent direct instantiation.
        name : str
            Name for the location.
        latitude : float
            Decimal degrees.
        longitude : float
            Decimal degrees.
        """
        assert class_private_create_key is NamedLocationGlobal.__create_key, "Use create() method."

        super().__init__(super()._LocationGlobal__create_key, latitude, longitude)

        self.name = name

    def __str__(self) -> str:
        """
        Convert to string representation.

        Returns
        -------
        str
            String representation of the NamedLocationGlobal object.
        """
        return f"{self.__class__}: name: {self.name}, latitude: {self.latitude}, longitude: {self.longitude}"
