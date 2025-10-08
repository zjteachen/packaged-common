"""
Wrapper for TCP client socket operations.
"""

import socket
from typing import Optional, Tuple

from .socket_wrapper import TcpSocket


class TcpClientSocket(TcpSocket):
    """
    Wrapper for TCP client socket operations.
    """

    __create_key = object()

    def __init__(self, class_private_create_key: object, socket_instance: socket.socket) -> None:
        """
        Private constructor, use create() method.

        Parameters
        ----------
        class_private_create_key : object
            Private key to ensure constructor is only called from create() method.
        socket_instance : socket.socket
            The socket instance to wrap.
        """

        assert class_private_create_key is TcpClientSocket.__create_key, "Use create() method"

        super().__init__(socket_instance=socket_instance)

    @classmethod
    def create(
        cls,
        instance: Optional[socket.socket] = None,
        host: str = "localhost",
        port: int = 5000,
        connection_timeout: float = 60.0,
    ) -> Tuple[bool, Optional["TcpClientSocket"]]:
        """
        Establishes socket connection through provided host and port.

        Parameters
        ----------
        instance : Optional[socket.socket], optional
            For initializing Socket with an existing socket object, by default None.
        host : str, optional
            The hostname or IP address to connect to, by default "localhost".
        port : int, optional
            The port number to connect to, by default 5000.
        connection_timeout : float, optional
            Timeout for establishing connection, in seconds, by default 60.0.

        Returns
        -------
        Tuple[bool, Optional[TcpClientSocket]]
            The first parameter represents if the socket creation is successful.
            - If it is not successful, the second parameter will be None.
            - If it is successful, the second parameter will be the created TcpClientSocket object.
        """

        # Reassign instance before check or Pylance will complain
        socket_instance = instance
        if socket_instance is not None:
            return True, TcpClientSocket(cls.__create_key, socket_instance)

        if connection_timeout <= 0:
            # Zero puts it on non-blocking mode, which complicates things
            print("Must be a positive non-zero value")
            return False, None

        try:
            socket_instance = socket.create_connection((host, port), connection_timeout)
            return True, TcpClientSocket(cls.__create_key, socket_instance)
        except TimeoutError:
            print("Connection timed out.")
        except socket.gaierror as e:
            print(
                f"Could not connect to socket, address related error: {e}. "
                "Make sure the host and port are correct."
            )
        except socket.error as e:
            print(f"Could not connect to socket, connection error: {e}.")

        return False, None
