"""
Decodes images from JPEG bytes to numpy array.
"""

import io

import numpy as np
from numpy.typing import NDArray
from PIL import Image


def decode(data: bytes) -> NDArray[np.uint8]:
    """
    Decodes a JPEG encoded image and returns it as a numpy array.

    Parameters
    ----------
    data : bytes
        Bytes object containing the JPEG encoded image.

    Returns
    -------
    NDArray[np.uint8]
        NDArray in RGB format. Shape is (Height, Width, 3).
    """
    image = Image.open(io.BytesIO(data), formats=["JPEG"])

    return np.asarray(image)
