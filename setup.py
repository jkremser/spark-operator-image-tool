#!/usr/bin/python3

from setuptools import setup, find_packages
import sys

if sys.version_info[0] != 3:
    sys.exit("\nPython3 is required in order to install soit")

setup(
    packages=find_packages()
)