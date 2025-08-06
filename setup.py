#!/usr/bin/env python3

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    if os.path.exists("README.md"):
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    return "USB Device Monitor - A system tray application for monitoring USB devices"

setup(
    name="usb-device-monitor",
    version="1.0.0",
    author="Daniel Gauthier",
    author_email="dan@usbconnectioninformation.com",
    description="A system tray application for monitoring USB devices in real-time",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/connection-information-suite/usb-connection-information-menubar-linux",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Hardware",
        "Topic :: System :: Monitoring",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyGObject>=3.36.0",
    ],
    extras_require={
        'dev': [
            'pytest>=6.0',
            'flake8>=3.8',
            'wheel>=0.37.0',
            'setuptools>=45.0.0',
        ],
    },
    entry_points={
        "console_scripts": [
            "usb-device-monitor=usb_device_monitor.main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
) 