"""
Encoding and Decoding Metadata
Save first byte as char to represent which worker sent the message
"""

import base64
import struct
from typing import Optional, Tuple

from . import worker_enum


DATA_FORMAT = "=Bi"  # 1 unsigned char + 1 int = 5 bytes


def encode_metadata(
    worker_id: worker_enum.WorkerEnum, number_of_messages: int
) -> Tuple[bool, Optional[bytes]]:
    """
    Encode metadata into a C-style string for STATUSTEXT message.
    Worker_ID to be encoded as the first byte of the message.

    Parameters
    ----------
    worker_id : worker_enum.WorkerEnum
        ID of the worker defined by its constant in WorkerEnum.
    number_of_messages : int
        Number of messages intended to be sent.

    Returns
    -------
    Tuple[bool, Optional[bytes]]
        Success status and encoded bytes containing number of messages.
        First byte depends on which worker is calling the function (its enum value).
        Returns (False, None) on encoding failure.
    """
    try:
        # Ensure worker ID is in the WorkerEnum class
        if not isinstance(worker_id, worker_enum.WorkerEnum):
            return False, None

        # Encode message using PositionGlobal's latitude, longitude, altitude, with the worker ID in the front
        packed_metadata = struct.pack(
            DATA_FORMAT,
            worker_id.value,
            number_of_messages,
        )

        # Encode in base64 so it can be put into a string
        encoded_str = base64.b64encode(packed_metadata)
    except (struct.error, AttributeError, ValueError):
        return False, None

    return True, encoded_str


def decode_metadata(
    encoded_str: bytes,
) -> Tuple[bool, Optional[worker_enum.WorkerEnum], Optional[int]]:
    """
    Decode bytes into metadata.

    Parameters
    ----------
    encoded_str : bytes
        Encoded bytearray containing Worker message ID and number of messages sent.

    Returns
    -------
    Tuple[bool, Optional[worker_enum.WorkerEnum], Optional[int]]
        Success status, WorkerEnum member instance corresponding to ID, and number of messages received.
        Returns (False, None, None) on decoding failure.
    """
    # Unpack the byte sequence
    try:
        # Decode base64
        encoded_metadata = base64.b64decode(encoded_str)

        # Ensure correct length (note the null terminator gets automatically dropped by STATUSTEXT)
        if len(encoded_metadata) != struct.calcsize(DATA_FORMAT):
            return False, None, None

        # unpack returns tuple (unsigned char,) so [0] is needed
        unpacked_data = struct.unpack(DATA_FORMAT, encoded_metadata)
        worker_id = worker_enum.WorkerEnum(unpacked_data[0])
        number_of_messages = unpacked_data[1]
    except struct.error:
        return False, None, None

    # Create and return a PositionGlobal object
    return True, worker_id, number_of_messages
