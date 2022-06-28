from setuptools import find_packages
from distutils.core import setup

setup(
    name='mini_gym',
    version='1.0.0',
    author='Gabriel Margolis',
    license="BSD-3-Clause",
    packages=find_packages(),
    author_email='gmargo@mit.edu',
    description='Isaac Gym environments for Legged Robots. Built on legged_gym by Nikita Rudin, ETH Zurich, NVIDIA',
    install_requires=[#'isaacgym',
                      'matplotlib',
                      'gym',
                      'ml_logger',
                      ]
)
