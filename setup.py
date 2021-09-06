import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

import unittest


def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover("tests", pattern="test_*.py")
    return test_suite


setuptools.setup(
    name="votesim",
    version="2.0.2",
    description="VoteSim is a python library for different voting methods",
    license="MIT",
    url="https://github.com/jss367/votesim",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    setup_requires=[],
    install_requires=[
        "tabulate",
    ],
    packages=setuptools.find_packages(exclude=["tests", "test_data"]),
    test_suite="setup.my_test_suite",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
