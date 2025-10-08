"""
Logger setup for `main()` .
"""

import datetime
import pathlib
from typing import Dict, Optional, Tuple

from . import logger


MAIN_LOGGER_NAME = "main"
MAX_ATTEMPTS = 3


def setup_main_logger(
    config: Dict,
    main_logger_name: str = MAIN_LOGGER_NAME,
    enable_log_to_file: bool = True,
    max_attempts: int = MAX_ATTEMPTS,
) -> Tuple[bool, Optional[logger.Logger], Optional[pathlib.Path]]:
    """
    Setup prerequisites for logging in `main()`.

    Parameters
    ----------
    config : Dict
        The configuration dictionary containing logger settings.
    main_logger_name : str, optional
        Name of the main logger, by default MAIN_LOGGER_NAME.
    enable_log_to_file : bool, optional
        Whether to enable logging to file, by default True.
    max_attempts : int, optional
        Maximum attempts to create unique log directory, by default MAX_ATTEMPTS.

    Returns
    -------
    Tuple[bool, Optional[logger.Logger], Optional[pathlib.Path]]
        Success status, logger instance (None if failed), and logger path (None if failed).
    """
    # Get settings
    try:
        log_directory_path = config["logger"]["directory_path"]
        log_path_format = config["logger"]["file_datetime_format"]
    except KeyError as exception:
        print(f"ERROR: Config key(s) not found: {exception}")
        return False, None, None

    # Create logging directory
    start_time = datetime.datetime.now()
    success = False
    for i in range(0, max_attempts):
        offset = datetime.timedelta(seconds=i)
        logging_path = pathlib.Path(
            log_directory_path, (start_time + offset).strftime(log_path_format)
        )
        if not logging_path.exists():
            success = True
            break

    if not success:
        print("ERROR: Could not create new log directory")

    logging_path.mkdir(exist_ok=False, parents=True)

    # Setup logger
    result, main_logger = logger.Logger.create(main_logger_name, enable_log_to_file)
    if not result:
        print("ERROR: Failed to create main logger")
        return False, None, None

    # Get Pylance to stop complaining
    assert main_logger is not None

    main_logger.info(f"{main_logger_name} logger initialized", True)

    return True, main_logger, logging_path
