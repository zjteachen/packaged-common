"""
Location on the ground in local Euclidean space (origin at home position global).

Class with name also available.
"""

from typing import Tuple, Literal, Optional


class LocationLocal:
    """
    Location in NED system relative to home position, with down = 0.0 .
    """

    __create_key = object()

    @classmethod
    def create(cls, north: float, east: float) -> Tuple[Literal[True], "LocationLocal"]:
        """
        Create a LocationLocal instance.

        Parameters
        ----------
        north : float
            Metres.
        east : float
            Metres.

        Returns
        -------
        Tuple[Literal[True], LocationLocal]
            Success status and the created LocationLocal object.
        """
        return True, LocationLocal(cls.__create_key, north, east)

    def __init__(self, class_private_create_key: object, north: float, east: float) -> None:
        """
        Private constructor, use create() method.

        Parameters
        ----------
        class_private_create_key : object
            Private key to prevent direct instantiation.
        north : float
            Metres.
        east : float
            Metres.
        """
        assert class_private_create_key is LocationLocal.__create_key, "Use create() method."

        self.north = north
        self.east = east

    def __str__(self) -> str:
        """
        Convert to string representation.

        Returns
        -------
        str
            String representation of the LocationLocal object.
        """
        return f"{self.__class__}: north: {self.north}, east: {self.east}"

    def __repr__(self) -> str:
        """
        Representation for collections (e.g. list).

        Returns
        -------
        str
            String representation of the LocationLocal object.
        """
        return str(self)


class NamedLocationLocal(LocationLocal):
    """
    Named LocationLocal.
    """

    __create_key = object()

    @classmethod
    # Additional argument for name
    # pylint: disable-next=arguments-differ
    def create(
        cls, name: str, north: float, east: float
    ) -> Tuple[Literal[True], "NamedLocationLocal"]:
        """
        Create a NamedLocationLocal instance.

        Parameters
        ----------
        name : str
            Name for the location. Can be empty.
        north : float
            Metres.
        east : float
            Metres.

        Returns
        -------
        Tuple[Literal[True], NamedLocationLocal]
            Success status and the created NamedLocationLocal object.
        """
        return True, NamedLocationLocal(cls.__create_key, name, north, east)

    def __init__(
        self, class_private_create_key: object, name: str, north: float, east: float
    ) -> None:
        """
        Private constructor, use create() method.

        Parameters
        ----------
        class_private_create_key : object
            Private key to prevent direct instantiation.
        name : str
            Name for the location.
        north : float
            Metres.
        east : float
            Metres.
        """
        assert class_private_create_key is NamedLocationLocal.__create_key, "Use create() method."

        super().__init__(super()._LocationLocal__create_key, north, east)

        self.name = name

    def __str__(self) -> str:
        """
        Convert to string representation.

        Returns
        -------
        str
            String representation of the NamedLocationLocal object.
        """
        return f"{self.__class__}: name: {self.name}, north: {self.north}, east: {self.east}"
