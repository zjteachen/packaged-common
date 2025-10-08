"""
Setup for HITL modules.
"""

import time
from threading import Event, Thread
from typing import Optional, Tuple
from modules.hitl.position_emulator import PositionEmulator
from modules.hitl.camera_emulator import CameraEmulator
from ..mavlink import dronekit


class HITL:
    """
    Hardware In The Loop (HITL) setup for emulating drone hardware.
    Provides a way to emulate the drone's position and camera input
    for testing purposes without needing actual hardware.
    """

    __create_key = object()

    @classmethod
    def create(
        cls,
        drone: dronekit.Vehicle,
        hitl_enabled: bool,
        position_module: bool,
        camera_module: bool,
        images_path: Optional[str] = None,
    ) -> Tuple[bool, Optional["HITL"]]:
        """
        Factory method to create a HITL instance.

        Parameters
        ----------
        drone : dronekit.Vehicle
            The dronekit instance to use for sending MAVLink messages.
        hitl_enabled : bool
            Boolean indicating if HITL is enabled.
        position_module : bool
            Boolean indicating if the position module is enabled.
        camera_module : bool
            Boolean indicating if the camera module is enabled.
        images_path : Optional[str], optional
            Path to the images directory for the camera emulator, by default None.

        Returns
        -------
        Tuple[bool, Optional[HITL]]
            A tuple containing success status and HITL instance (or None if failed).
        """
        if not isinstance(drone, dronekit.Vehicle):
            return False, None

        if not hitl_enabled:
            return True, HITL(cls.__create_key, drone, None, None)

        if position_module:
            result, position_emulator = PositionEmulator.create(drone)
            if not result:
                return False, None

        if camera_module:
            result, camera_emulator = CameraEmulator.create(images_path)
            if not result:
                return False, None

        hitl = HITL(
            cls.__create_key,
            drone,
            position_emulator if position_module else None,
            camera_emulator if camera_module else None,
        )

        return True, hitl

    def __init__(
        self,
        class_private_create_key: object,
        drone: dronekit.Vehicle,
        position_emulator: Optional[PositionEmulator] = None,
        camera_emulator: Optional[CameraEmulator] = None,
    ) -> None:
        """
        Private constructor, use create() method.

        Parameters
        ----------
        class_private_create_key : object
            Private key to ensure constructor is only called via create().
        drone : dronekit.Vehicle
            The dronekit instance to use for sending MAVLink messages.
        position_emulator : Optional[PositionEmulator], optional
            Position emulator instance, by default None.
        camera_emulator : Optional[CameraEmulator], optional
            Camera emulator instance, by default None.
        """
        assert class_private_create_key is HITL.__create_key, "Use create() method"

        self.drone = drone
        self.position_emulator = position_emulator
        self.camera_emulator = camera_emulator

        self._stop_event: Optional[Event] = None
        self._threads: list[Thread] = []

    def start(self) -> None:
        """
        Start HITL module threads.

        Creates and starts daemon threads for position and camera emulation
        if their respective emulators are enabled.
        """
        if self._stop_event is not None:
            return

        self._stop_event = Event()
        self._threads = []

        if self.position_emulator is not None:
            t = Thread(target=self.run_position, name="HITL-Position", daemon=True)
            self._threads.append(t)
            t.start()

        if self.camera_emulator is not None:
            t = Thread(target=self.run_camera, name="HITL-Camera", daemon=True)
            self._threads.append(t)
            t.start()

    def shutdown(self, join_timeout: Optional[float] = 5.0) -> None:
        """
        Signal threads to stop and join them.

        Parameters
        ----------
        join_timeout : Optional[float], optional
            Timeout in seconds for joining threads, by default 5.0.
        """
        if self._stop_event is None:
            return

        self._stop_event.set()

        for t in self._threads:
            if t.is_alive():
                t.join(timeout=join_timeout)

        self._threads.clear()
        self._stop_event = None

    def __del__(self) -> None:
        """
        Best-effort cleanup when HITL object is destroyed.

        Ensures threads are stopped and the drone connection is closed.
        This is a destructor that performs cleanup during garbage collection.
        """
        try:
            self.shutdown()
        except Exception:  # pylint: disable=broad-except
            pass

    def run_position(self) -> None:
        """
        Run the position emulator periodic function in a loop.

        This method is intended to be executed in a separate thread.
        It continuously calls the position emulator's periodic() method
        until the stop event is set.
        """
        assert self._stop_event is not None
        while not self._stop_event.is_set():
            try:
                self.position_emulator.periodic()
            except Exception as exc:  # pylint: disable=broad-except
                print(f"HITL position thread error: {exc}")
                time.sleep(0.1)

    def run_camera(self) -> None:
        """
        Run the camera emulator periodic function in a loop.

        This method is intended to be executed in a separate thread.
        It continuously calls the camera emulator's periodic() method
        until the stop event is set.
        """
        assert self._stop_event is not None
        while not self._stop_event.is_set():
            try:
                self.camera_emulator.periodic()
            except Exception as exc:  # pylint: disable=broad-except
                print(f"HITL camera thread error: {exc}")
                time.sleep(0.1)
