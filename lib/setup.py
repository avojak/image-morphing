from setuptools import setup

setup(
    name='libmorphing',
    version='0.0.1',
    author='Andrew Vojak',
    author_email='andrew.vojak@gmail.com',
    description='Implementation of image morphing',
    license='Apache License, Version 2.0',
    url='https://github.com/avojak/image-morphing',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    packages=['libmorphing']
)