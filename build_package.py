#!/usr/bin/env python3
"""
Script to build warg_common Python package with selected modules.

This script copies specified modules from the modules/ folder into a warg_common/
package directory, then builds a Python wheel that gets output to dist/.

Usage:
    python build_package.py [module1] [module2] ...

Example:
    python build_package.py camera network logger
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def clean_build_directories():
    """Remove existing build artifacts."""
    dirs_to_clean = ["warg_common", "build", "dist", "*.egg-info"]
    for dir_pattern in dirs_to_clean:
        for path in Path(".").glob(dir_pattern):
            if path.exists():
                print(f"Cleaning {path}")
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()


def copy_module(module_name: str, source_dir: Path, target_dir: Path):
    """Copy a module from source to target directory."""
    source_module = source_dir / module_name

    if not source_module.exists():
        print(f"Warning: Module '{module_name}' not found in {source_dir}")
        return False

    target_module = target_dir / module_name

    if source_module.is_dir():
        shutil.copytree(source_module, target_module)
        print(f"Copied module: {module_name}/")
    else:
        shutil.copy2(source_module, target_module)
        print(f"Copied module: {module_name}")

    return True


def create_package_structure(modules: list[str]):
    """Create the warg_common package structure with specified modules."""
    warg_common_dir = Path("warg_common")
    warg_common_dir.mkdir(exist_ok=True)

    # Create __init__.py for the package
    init_file = warg_common_dir / "__init__.py"
    init_file.write_text(
        '"""WARG Common package with shared modules."""\n\n__version__ = "0.1.0"\n'
    )

    # Copy each specified module
    modules_dir = Path("modules")
    copied_modules = []

    for module in modules:
        if copy_module(module, modules_dir, warg_common_dir):
            copied_modules.append(module)

    # Copy module-level files if they exist
    for file_name in ["__init__.py"] + [
        f for f in modules_dir.glob("*.py") if f.name != "__init__.py"
    ]:
        if file_name == "__init__.py":
            continue  # We already created our own __init__.py
        source_file = modules_dir / file_name if isinstance(file_name, str) else file_name
        if source_file.exists() and source_file.is_file():
            target_file = warg_common_dir / source_file.name
            shutil.copy2(source_file, target_file)
            print(f"Copied: {source_file.name}")

    return copied_modules


def build_wheel():
    """Build the Python wheel package."""
    print("\nBuilding wheel...")
    result = subprocess.run(
        [sys.executable, "-m", "build", "--wheel"],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        print("✓ Wheel built successfully!")
        print(f"\nOutput in dist/:")
        for wheel in Path("dist").glob("*.whl"):
            print(f"  - {wheel.name}")
        return True
    else:
        print("✗ Build failed!")
        print(result.stderr)
        return False


def generate_modules_rst(copied_modules: list[str]):
    """Generate modules.rst based on which modules were actually copied."""
    # Module documentation templates
    module_docs = {
        "camera": """
Camera Module
-------------

.. automodule:: warg_common.camera
   :members:
   :undoc-members:
   :show-inheritance:
""",
        "network": """
Network Module
--------------

TCP
~~~

.. automodule:: warg_common.network.tcp
   :members:
   :undoc-members:
   :show-inheritance:

UDP
~~~

.. automodule:: warg_common.network.udp
   :members:
   :undoc-members:
   :show-inheritance:
""",
        "logger": """
Logger Module
-------------

.. automodule:: warg_common.logger
   :members:
   :undoc-members:
   :show-inheritance:
""",
        "data_encoding": """
Data Encoding Module
--------------------

.. automodule:: warg_common.data_encoding
   :members:
   :undoc-members:
   :show-inheritance:
""",
        "image_encoding": """
Image Encoding Module
---------------------

.. automodule:: warg_common.image_encoding
   :members:
   :undoc-members:
   :show-inheritance:
""",
        "qr": """
QR Module
---------

.. automodule:: warg_common.qr
   :members:
   :undoc-members:
   :show-inheritance:
""",
        "kml": """
KML Module
----------

.. automodule:: warg_common.kml
   :members:
   :undoc-members:
   :show-inheritance:
""",
        "read_yaml": """
Read YAML Module
----------------

.. automodule:: warg_common.read_yaml
   :members:
   :undoc-members:
   :show-inheritance:
""",
        "hitl": """
HITL Module
-----------

.. automodule:: warg_common.hitl
   :members:
   :undoc-members:
   :show-inheritance:
""",
        "mavlink": """
MAVLink Module
--------------

.. automodule:: warg_common.mavlink
   :members:
   :undoc-members:
   :show-inheritance:
""",
    }

    # Build the modules.rst content
    content = ["API Reference", "=============", "",
               "This page contains the API reference for all modules in the WARG Common package.", ""]

    # Add documentation for each copied module
    for module in copied_modules:
        if module in module_docs:
            content.append(module_docs[module])

    # Always include data types section (these are standalone files)
    content.append("""
Data Types
----------

Location (Global)
~~~~~~~~~~~~~~~~~

.. automodule:: warg_common.location_global
   :members:
   :undoc-members:
   :show-inheritance:

Location (Local)
~~~~~~~~~~~~~~~~

.. automodule:: warg_common.location_local
   :members:
   :undoc-members:
   :show-inheritance:

Position (Global)
~~~~~~~~~~~~~~~~~

.. automodule:: warg_common.position_global
   :members:
   :undoc-members:
   :show-inheritance:

Position (Global Relative Altitude)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: warg_common.position_global_relative_altitude
   :members:
   :undoc-members:
   :show-inheritance:

Position (Local)
~~~~~~~~~~~~~~~~

.. automodule:: warg_common.position_local
   :members:
   :undoc-members:
   :show-inheritance:

Orientation
~~~~~~~~~~~

.. automodule:: warg_common.orientation
   :members:
   :undoc-members:
   :show-inheritance:
""")

    # Write the generated content
    modules_rst_path = Path("docs/modules.rst")
    modules_rst_path.write_text("\n".join(content))
    print(f"Generated modules.rst with {len(copied_modules)} module(s)")


def build_docs(copied_modules: list[str]):
    """Build Sphinx documentation and copy to dist/."""
    print("\nBuilding documentation...")

    # Generate modules.rst based on what was copied
    generate_modules_rst(copied_modules)

    # Clean previous docs build
    docs_build_dir = Path("docs/_build")
    if docs_build_dir.exists():
        shutil.rmtree(docs_build_dir)

    # Build HTML documentation
    result = subprocess.run(
        [sys.executable, "-m", "sphinx", "-b", "html", "docs", "docs/_build/html"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print("✗ Documentation build failed!")
        print(result.stderr)
        return False

    # Copy documentation to dist/
    dist_docs_dir = Path("dist/docs")
    if dist_docs_dir.exists():
        shutil.rmtree(dist_docs_dir)

    shutil.copytree(Path("docs/_build/html"), dist_docs_dir)

    print("✓ Documentation built successfully!")
    print(f"  - HTML documentation: dist/docs/index.html")
    return True


def main():
    parser = argparse.ArgumentParser(description="Build warg_common package with selected modules")
    parser.add_argument(
        "modules", nargs="+", help="Modules to include in the package (e.g., camera network logger)"
    )
    parser.add_argument(
        "--no-clean", action="store_true", help="Don't clean build directories before building"
    )
    parser.add_argument(
        "--docs", action="store_true", help="Build Sphinx documentation"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("WARG Common Package Builder")
    print("=" * 60)

    # Clean existing build artifacts
    if not args.no_clean:
        print("\nCleaning build directories...")
        clean_build_directories()

    # Create package structure
    print(f"\nCreating package structure with modules: {', '.join(args.modules)}")
    copied_modules = create_package_structure(args.modules)

    if not copied_modules:
        print("\nError: No modules were copied. Aborting build.")
        sys.exit(1)

    print(f"\nSuccessfully prepared {len(copied_modules)} module(s)")

    # Build the wheel
    wheel_success = build_wheel()

    # Build documentation if requested
    docs_success = True
    if args.docs:
        docs_success = build_docs(copied_modules)

    print("\n" + "=" * 60)
    if wheel_success and docs_success:
        print("Build completed successfully!")
        if args.docs:
            print("\nTo view the documentation, open: dist/docs/index.html")
    else:
        print("Build failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
