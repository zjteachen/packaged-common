"""
Converts an image containing QR codes into text.
"""

from typing import Optional, Tuple

import numpy as np
from numpy.typing import NDArray
from pyzbar import pyzbar


class QrScanner:
    """
    Wrapper for pyzbar.
    """

    def __init__(self) -> None:
        """
        Nothing to do.
        """

    @staticmethod
    def get_qr_text(frame: NDArray[np.uint8]) -> Tuple[bool, Optional[str]]:
        """
        Attempts to find and decode a QR code from the given frame.

        Parameters
        ----------
        frame : NDArray[np.uint8]
            The image frame to scan for QR codes.

        Returns
        -------
        Tuple[bool, Optional[str]]
            Success status and the decoded QR code text.
            Returns (False, None) if no QR code is found.
        """
        decoded_qrs = pyzbar.decode(frame)
        if len(decoded_qrs) == 0:
            return False, None

        qr_text = decoded_qrs[0].data.decode()
        return True, qr_text
