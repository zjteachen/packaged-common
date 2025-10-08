"""
For YAML files.
"""

import pathlib
from typing import Any, Dict, Optional, Tuple

import yaml


def open_config(file_path: pathlib.Path) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Open and decode YAML file.

    Parameters
    ----------
    file_path : pathlib.Path
        Path to the YAML configuration file.

    Returns
    -------
    Tuple[bool, Optional[Dict[str, Any]]]
        Success status and the parsed YAML configuration dictionary if successful,
        None otherwise.
    """
    try:
        with file_path.open("r", encoding="utf8") as file:
            try:
                config = yaml.safe_load(file)
                return True, config
            except yaml.YAMLError as exception:
                print(f"ERROR: Could not parse YAML file: {exception}")
    except FileNotFoundError as exception:
        print(f"ERROR: YAML file not found: {exception}")
    except IOError as exception:
        print(f"ERROR: Could not open file: {exception}")

    return False, None
