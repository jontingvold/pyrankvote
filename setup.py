import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
import unittest
def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite

setuptools.setup(
    name='pyrankvote',
    version='1.0.9',
    author='Jon Tingvold',
    author_email='jon.tingvold@gmail.com',
    description='PyRankVote is a python library for different ranked voting methods, '
                'like instant-runoff voting, single transferable vote and preferential block voting, '
                'created by Jon Tingvold.',
    license='MIT',
    url='https://github.com/jontingvold/pyrankvote',
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
    setup_requires=[],
    install_requires=[
        'tabulate',
    ],
    
    packages=setuptools.find_packages(exclude=['tests']),
    
    test_suite="setup.my_test_suite",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
