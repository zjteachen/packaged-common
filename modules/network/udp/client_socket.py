"""
Wrapper for UDP client socket operations.
"""

import socket
from typing import Optional, Tuple

from .socket_wrapper import UdpSocket


class UdpClientSocket(UdpSocket):
    """
    Wrapper for UDP client socket operations.
    """

    __create_key = object()

    def __init__(
        self,
        class_private_create_key: object,
        socket_instance: socket.socket,
        server_address: Tuple[str, int],
    ) -> None:
        """
        Private Constructor, use create() method.

        Parameters
        ----------
        class_private_create_key : object
            Private key to ensure constructor is only called from create() method.
        socket_instance : socket.socket
            The socket instance to wrap.
        server_address : Tuple[str, int]
            The server address as (host, port).
        """

        assert class_private_create_key is UdpClientSocket.__create_key

        super().__init__(socket_instance=socket_instance)
        self.__server_address = server_address

    @classmethod
    def create(
        cls, host: str = "localhost", port: int = 5000, connection_timeout: float = 60.0
    ) -> Tuple[bool, Optional["UdpClientSocket"]]:
        """
        Initializes UDP client socket with the appropriate server address.

        Parameters
        ----------
        host : str, optional
            The hostname or IP address of the server, by default "localhost".
        port : int, optional
            The port number of the server, by default 5000.
        connection_timeout : float, optional
            Timeout for establishing connection, in seconds, by default 60.0.

        Returns
        -------
        Tuple[bool, Optional[UdpClientSocket]]
            The boolean value represents whether the initialization was successful or not.
            - If it is not successful, the second parameter will be None.
            - If it is successful, the method will return True and a UdpClientSocket object will be created.
        """

        if connection_timeout <= 0:
            print("Must provide positive non-zero value.")
            return False, None

        try:
            socket_instance = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            socket_instance.settimeout(connection_timeout)
            server_address = (host, port)
            return True, UdpClientSocket(cls.__create_key, socket_instance, server_address)
        except TimeoutError as e:
            print(f"Connection timed out: {e}")

        except socket.gaierror as e:
            print(
                f"Could not connect to socket, address related error: {e}. Make sure the host and port are correct."
            )

        except socket.error as e:
            print(f"Could not connect: {e}")

        return False, None

    def send(self, data: bytes) -> bool:
        """
        Sends data to the specified server address during this socket's creation.

        Parameters
        ----------
        data : bytes
            The raw data to send.

        Returns
        -------
        bool
            True if data is sent successfully, False if it fails to send.
        """

        try:
            host, port = self.__server_address
            super().send_to(data, host, port)
        except socket.error as e:
            print(f"Could not send data: {e}")
            return False

        return True

    def recv(self, buf_size: int) -> None:
        """
        Receive data method override to prevent client sockets from receiving data.

        Parameters
        ----------
        buf_size : int
            The amount of data to be received.

        Raises
        ------
        NotImplementedError
            Always raised because client sockets should not receive data.
        """

        raise NotImplementedError(
            "Client sockets cannot receive data as they are not bound by a port."
        )
