"""
Position in local Euclidean space (origin at home position global).
"""

from typing import Tuple, Literal, Optional


class PositionLocal:
    """
    Position in NED system relative to home position.
    """

    __create_key = object()

    @classmethod
    def create(
        cls, north: float, east: float, down: float
    ) -> Tuple[Literal[True], "PositionLocal"]:
        """
        Create a PositionLocal instance.

        Parameters
        ----------
        north : float
            Metres.
        east : float
            Metres.
        down : float
            Metres. Allowed to be positive, which is below the home position.

        Returns
        -------
        Tuple[Literal[True], PositionLocal]
            Success status and the created PositionLocal object.
        """
        return True, PositionLocal(cls.__create_key, north, east, down)

    def __init__(
        self, class_private_create_key: object, north: float, east: float, down: float
    ) -> None:
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
        down : float
            Metres. Allowed to be positive, which is below the home position.
        """
        assert class_private_create_key is PositionLocal.__create_key, "Use create() method."

        self.north = north
        self.east = east
        self.down = down

    def __str__(self) -> str:
        """
        Convert to string representation.

        Returns
        -------
        str
            String representation of the PositionLocal object.
        """
        return f"{self.__class__}: north: {self.north}, east: {self.east}, down: {self.down}"

    def __repr__(self) -> str:
        """
        Representation for collections (e.g. list).

        Returns
        -------
        str
            String representation of the PositionLocal object.
        """
        return str(self)


class NamedPositionLocal(PositionLocal):
    """
    Named PositionLocal.
    """

    __create_key = object()

    @classmethod
    # Additional argument for name
    # pylint: disable-next=arguments-differ
    def create(
        cls,
        name: str,
        north: float,
        east: float,
        down: float,
    ) -> Tuple[Literal[True], "NamedPositionLocal"]:
        """
        Create a NamedPositionLocal instance.

        Parameters
        ----------
        name : str
            Name for the position. Can be empty.
        north : float
            Metres.
        east : float
            Metres.
        down : float
            Metres. Allowed to be positive, which is below the home position.

        Returns
        -------
        Tuple[Literal[True], NamedPositionLocal]
            Success status and the created NamedPositionLocal object.
        """
        return True, NamedPositionLocal(cls.__create_key, name, north, east, down)

    def __init__(
        self, class_private_create_key: object, name: str, north: float, east: float, down: float
    ) -> None:
        """
        Private constructor, use create() method.

        Parameters
        ----------
        class_private_create_key : object
            Private key to prevent direct instantiation.
        name : str
            Name for the position.
        north : float
            Metres.
        east : float
            Metres.
        down : float
            Metres. Allowed to be positive, which is below the home position.
        """
        assert class_private_create_key is NamedPositionLocal.__create_key, "Use create() method."

        super().__init__(super()._PositionLocal__create_key, north, east, down)

        self.name = name

    def __str__(self) -> str:
        """
        Convert to string representation.

        Returns
        -------
        str
            String representation of the NamedPositionLocal object.
        """
        return f"{self.__class__}: name: {self.name}, north: {self.north}, east: {self.east}, down: {self.down}"
