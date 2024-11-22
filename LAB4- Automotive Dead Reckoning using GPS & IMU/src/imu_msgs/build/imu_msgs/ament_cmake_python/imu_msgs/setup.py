from setuptools import find_packages
from setuptools import setup

setup(
    name='imu_msgs',
    version='0.0.0',
    packages=find_packages(
        include=('imu_msgs', 'imu_msgs.*')),
)
