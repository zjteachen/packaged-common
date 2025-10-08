"""
Decodes a numpy array and returns a JPEG encoded image
"""

import io

import numpy as np
from numpy.typing import NDArray
from PIL import Image


QUALITY = 80  # Quality of JPEG encoding to use (0-100)


def encode(image_array: NDArray[np.uint8]) -> bytes:
    """
    Encodes an image in numpy array form into bytes of a JPEG.

    Parameters
    ----------
    image_array : NDArray[np.uint8]
        Numpy array of an RGB image with shape (Height, Width, 3).

    Returns
    -------
    bytes
        Bytes which form the JPEG encoded image.
    """
    img = Image.fromarray(image_array, mode="RGB")

    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=QUALITY)

    return buffer.getvalue()
