"""
Emulates camera input to PI.

Requires OBS Virtual Camera on Windows or
v4l2loopback for Linux to be installed to work
"""

import os
import time
from typing import Optional, Tuple
import pyvirtualcam
import cv2
from numpy.typing import NDArray

IMAGE_SIZE = (720, 480)
IMAGE_FORMATS = (".png", ".jpeg", "jpg")
CAMERA_FPS = 30


class CameraEmulator:
    """
    Setup for camera emulator.
    """

    __create_key = object()

    @classmethod
    def create(
        cls, images_path: str, time_between_images: float = 1.0
    ) -> Tuple[bool, Optional["CameraEmulator"]]:
        """
        Set up camera emulator.

        Parameters
        ----------
        images_path : str
            Path to the directory containing images for the camera emulator.
            Cycles through these images to simulate camera input.
        time_between_images : float, optional
            Time in seconds between image changes, by default 1.0.

        Returns
        -------
        Tuple[bool, Optional[CameraEmulator]]
            A tuple containing success status and CameraEmulator instance (or None if failed).
        """

        if not isinstance(images_path, str):
            print("Images path is not a string")
            return False, None

        if not os.path.isdir(images_path):
            print("Images path is not a valid directory")
            return False, None

        if not isinstance(time_between_images, (int, float)):
            print("Time between images is not a number")
            return False, None

        if time_between_images <= 0:
            print("Time between images must be positive")
            return False, None

        try:
            virtual_camera_instance = pyvirtualcam.Camera(IMAGE_SIZE[0], IMAGE_SIZE[1], CAMERA_FPS)

        # Required for catching library exceptions
        # pylint: disable-next=broad-exception-caught
        except Exception as e:
            print(
                "Error creating virtual camera (Check if OBS or v4l2loopback is installed): "
                + str(e)
            )
            return False, None

        if virtual_camera_instance is None:
            return False, None

        return True, CameraEmulator(
            cls.__create_key, images_path, time_between_images, virtual_camera_instance
        )

    def __init__(
        self,
        class_private_create_key: object,
        images_path: str,
        time_between_images: float,
        virtual_camera: pyvirtualcam.Camera,
    ) -> None:
        """
        Private constructor, use create() method.

        Parameters
        ----------
        class_private_create_key : object
            Private key to ensure constructor is only called via create().
        images_path : str
            Path to the directory containing images.
        time_between_images : float
            Time in seconds between image changes.
        virtual_camera : pyvirtualcam.Camera
            The virtual camera instance.
        """
        assert class_private_create_key is CameraEmulator.__create_key, "Use create() method"

        self.__image_folder_path = images_path
        self.__virtual_camera = virtual_camera
        self.__image_paths: list[str] = []
        self.__current_frame: Optional[NDArray] = None
        self.__image_index = 0
        self.__next_image_time = time.time() + time_between_images
        self.__time_between_images = time_between_images

        self.__get_images()
        self.update_current_image()

    def periodic(self) -> None:
        """
        Execute periodic camera emulation tasks.

        Sends frames to the virtual camera and cycles through images
        at the specified interval.
        """
        try:
            # Send frame and pace to target FPS
            self.send_frame()
            self.sleep_until_next_frame()

            now = time.time()
            if now >= self.__next_image_time:
                # Cycle image once per second
                try:
                    self.next_image()
                    self.update_current_image()
                except Exception as exc:  # pylint: disable=broad-except
                    print(f"HITL camera image update error: {exc}")
                self.__next_image_time = now + self.__time_between_images
        except Exception as exc:  # pylint: disable=broad-except
            print(f"HITL camera periodic error: {exc}")

    def send_frame(self) -> None:
        """
        Send a new frame to virtual camera.

        This method should be called in a loop to maintain the video stream.
        """
        try:
            self.__virtual_camera.send(self.__current_frame)

        # Required for catching library exceptions
        # pylint: disable-next=broad-exception-caught
        except Exception as e:
            print("Cannot send frame" + str(e))

    def sleep_until_next_frame(self) -> None:
        """
        Wait an amount of time to maintain targeted framerate.

        This is a wrapper for pyvirtualcam's sleep_until_next_frame method.
        """
        self.__virtual_camera.sleep_until_next_frame()

    def update_current_image(self) -> None:
        """
        Set current image to the image specified by the current image index.

        Reads the image from disk, converts it to RGB format, and updates
        the current frame. Skips images that fail to load.
        """

        has_image = False
        loop_count = 0

        # loop to skip image if read fails
        while not has_image and loop_count < len(self.__image_paths):
            try:
                image_path = self.__image_paths[self.__image_index]
                image = cv2.imread(image_path)
                self.__current_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                has_image = True

            # Required for catching library exceptions
            # pylint: disable-next=broad-exception-caught
            except Exception as e:
                print("Could not read image: " + image_path + " Error: " + str(e))
                self.next_image()
                loop_count += 1

    def next_image(self) -> None:
        """
        Increment image index by 1.

        Wraps around to the beginning when reaching the end of the image list.
        """

        self.__image_index = (self.__image_index + 1) % len(self.__image_paths)

    def __get_images(self) -> None:
        """
        Populate the images array with paths of all images in the folder.

        Scans the image folder for files with valid image formats and stores
        their paths in the internal image paths list.
        """
        try:
            for image in os.listdir(self.__image_folder_path):
                if image.endswith(IMAGE_FORMATS):
                    path = os.path.join(self.__image_folder_path, image)
                    self.__image_paths.append(path)

        # Required for catching library exceptions
        # pylint: disable-next=broad-exception-caught
        except Exception as e:
            print("Error reading images: " + str(e))
