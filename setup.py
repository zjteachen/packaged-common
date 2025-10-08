from setuptools import setup

setup(
    name="warg_common",
    version="0.1.0",
    description="Abstractions for use across WARG's repositories.",
    author="WARG",
    author_email="t47chen@uwaterloo.ca",
    packages=["warg_common"],
    install_requires=[
        "fastcrc==0.3.2",
        "lxml==6.0.2",
        "monotonic==1.6",
        "pymavlink==2.4.49",
    ],
)
