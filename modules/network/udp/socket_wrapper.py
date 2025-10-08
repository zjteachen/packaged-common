"""
Wrapper for a UDP socket.
"""

import socket
import time
from typing import Optional, Tuple


CHUNK_SIZE = 2**15  # 32 kb, may need to be shrunk on pi becasue its buffer may not be as large
SEND_DELAY = 1e-4  # Delay in seconds in between sends to avoid filling socket buffer


class UdpSocket:
    """
    Wrapper for a UDP socket.
    """

    def __init__(self, socket_instance: Optional[socket.socket] = None) -> None:
        """
        Initialize the UdpSocket wrapper.

        Parameters
        ----------
        socket_instance : Optional[socket.socket], optional
            For initializing Socket with an existing socket object, by default None.
        """

        self.__socket = socket_instance

    def send_to(
        self,
        data: bytes,
        host: str = "",
        port: int = 5000,
        chunk_size: int = CHUNK_SIZE,
        send_delay: float = SEND_DELAY,
    ) -> bool:
        """
        Sends data to specified address.

        Parameters
        ----------
        data : bytes
            The data to send.
        host : str, optional
            Empty string is interpreted as '0.0.0.0' (IPv4) or '::' (IPv6), which is an open address, by default "".
        port : int, optional
            The port number to send to, by default 5000.
        chunk_size : int, optional
            Size of data chunks to send, by default CHUNK_SIZE.
        send_delay : float, optional
            Delay in seconds between sends to avoid filling socket buffer, by default SEND_DELAY.

        Returns
        -------
        bool
            True if data was transferred successfully, False otherwise.
        """

        address = (host, port)
        data_sent = 0
        data_size = len(data)

        while data_sent < data_size:
            if data_sent + chunk_size > data_size:
                chunk = data[data_sent:data_size]
            else:
                chunk = data[data_sent : data_sent + chunk_size]

            try:
                self.__socket.sendto(chunk, address)
                data_sent += len(chunk)
            except socket.error as e:
                print(f"Could not send data: {e}")
                return False

            time.sleep(send_delay)

        return True

    def recv(self, buf_size: int) -> Tuple[bool, Optional[bytes]]:
        """
        Receives data from the socket.

        Parameters
        ----------
        buf_size : int
            The number of bytes to receive.

        Returns
        -------
        Tuple[bool, Optional[bytes]]
            First element is True if data was received successfully, False otherwise.
            Second element is the received data, or None if unsuccessful.
        """

        data = b""
        addr = None
        data_size = 0

        while data_size < buf_size:
            try:
                packet, current_addr = self.__socket.recvfrom(buf_size)
                if addr is None:
                    addr = current_addr
                elif addr != current_addr:
                    print(f"Data received from multiple addresses: {addr} and {current_addr}")
                    packet = b""

                # Add the received packet to the accumulated data and increment the size accordingly
                data += packet
                data_size += len(packet)

            except socket.error as e:
                print(f"Could not receive data: {e}")
                return False, None

        return True, data

    def get_socket(self) -> socket.socket:
        """
        Getter for the underlying socket object.

        Returns
        -------
        socket.socket
            The underlying socket object.
        """

        return self.__socket
