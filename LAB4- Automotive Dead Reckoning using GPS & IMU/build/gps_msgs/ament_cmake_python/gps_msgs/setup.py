from setuptools import find_packages
from setuptools import setup

setup(
    name='gps_msgs',
    version='0.0.1',
    packages=find_packages(
        include=('gps_msgs', 'gps_msgs.*')),
)
