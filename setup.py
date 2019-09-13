import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyrankvote',
    version='1.0.0',
    author='Jon Tingvold',
    author_email='jon.tingvold@gmail.com',
    description='PyRankVote is a python library for different ranked voting methods, '
                'like instant-runoff voting, single transferable vote and preferential block voting, '
                'created by Jon Tingvold.',
    license='MIT',
    url='https://github.com/jontingvold/pyrankvote',

    long_description=long_description,
    long_description_content_type="text/markdown",
    setup_requires=[],
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
