# WARG Common

**This is a fork of common intended to facilitate package building and automatic documentation generation.**

Common code shared across WARG repositories, packaged as `warg_common` with modular builds and auto-generated Sphinx documentation.

## Features

- **Modular Package Building**: Select only the modules you need
- **Automatic Documentation**: Sphinx-generated HTML docs from Numpy-style docstrings
- **Type-Annotated**: Full type hints using Python's typing module
- **Well-Documented**: Comprehensive Numpy-style docstrings for all modules

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd common
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
```

### 3. Install Dependencies

```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Building the Package

### Basic Package Build

Build a wheel with selected modules:

```bash
python build_package.py camera network logger
```

This will:

- Copy the specified modules to `warg_common/`
- Build a wheel at `dist/warg_common-0.1.0-py3-none-any.whl`

### Available Modules

- `camera` - Camera device abstractions (OpenCV, PiCamera2, ArducamIR)
- `network` - TCP/UDP socket wrappers
- `logger` - Logging utilities
- `data_encoding` - Position/metadata encoding/decoding
- `image_encoding` - JPEG image encoding/decoding
- `qr` - QR code scanner
- `kml` - KML file generation
- `hitl` - Hardware-in-the-loop testing
- `mavlink` - MAVLink flight controller interface
- `read_yaml` - YAML configuration reader

**Note:** Position, location, and orientation data types are always included as they're used across modules.

### Build with Documentation

```bash
python build_package.py camera network logger --docs
```

This generates:

- Package wheel: `dist/warg_common-0.1.0-py3-none-any.whl`
- HTML documentation: `dist/docs/index.html`

Open `dist/docs/index.html` in a browser to view the documentation.

### Build Options

```bash
# Build without cleaning previous builds
python build_package.py camera --no-clean

# Build all modules with documentation
python build_package.py camera network logger data_encoding image_encoding qr kml hitl mavlink read_yaml --docs
```

## Using the Package

### Installation

The build file creates a wheel file in the `dist` folder. This file can simply be pip installed in any other projects.

```bash
# create a venv
python -m venv venv/
# install wheel
pip install path/to/wheel/file.whl
```

### Usage Examples

#### Camera Module

```python
from warg_common.camera import CameraOpenCV, ConfigOpenCV, CameraOption

# Create OpenCV camera
config = ConfigOpenCV(device_index=0)
success, camera = CameraOpenCV.create(width=1920, height=1080, config=config)

if success:
    # Capture image
    result, image = camera.run()
    if result:
        print(f"Captured image shape: {image.shape}")
```

#### Network Module

```python
from warg_common.network.tcp import TcpClientSocket

# Connect to TCP server
success, client = TcpClientSocket.create(host="localhost", port=5000)

if success:
    # Send data
    client.send(b"Hello, server!")

    # Receive data
    success, data = client.recv(1024)
    if success:
        print(f"Received: {data}")

    client.close()
```

#### Logger Module

```python
from warg_common.logger import Logger

# Create logger
success, logger = Logger.create(name="my_app", enable_log_to_file=False)

if success:
    logger.info("Application started")
    logger.warning("This is a warning")
    logger.error("An error occurred")
```

## Development

### Documentation Structure

- `docs/conf.py` - Sphinx configuration with Numpy docstring support
- `docs/index.rst` - Main documentation page
- `docs/modules.rst` - Auto-generated API reference (created during build)

### Docstring Format

All modules use Numpy-style docstrings:

```python
def example_function(param1: int, param2: str) -> Tuple[bool, Optional[str]]:
    """
    Short description of function.

    Parameters
    ----------
    param1 : int
        Description of param1.
    param2 : str
        Description of param2.

    Returns
    -------
    Tuple[bool, Optional[str]]
        Success status and result string if successful, None otherwise.
    """
    pass
```
