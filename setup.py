"""Install script for setuptools."""

from setuptools import find_packages
from setuptools import setup

setup(
    name='digital_brain',
    version='1.0.0',
    description='An implementation of the pipeline and interaction within the Digital Brain'
                'This is a collection of models and pipelines that are meant to interact with each other in a cohesive manner',
    author='Michael Bahchevanov',
    author_email='bahchevanov.mihail@gmail.com',
    url='https://github.com/michaelbahchevanov/digital-brain',
    packages=find_packages(),
    install_requires=[
        numpy
    ],
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.9',
        'Topic :: Engineering :: Artificial Intelligence'
    ],
)