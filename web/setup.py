from setuptools import setup

with open('VERSION') as version_file:
    version = version_file.read().strip()

setup(
    name='webmorphing',
    version=version,
    author='Andrew Vojak',
    author_email='andrew.vojak@gmail.com',
    description='Web service for image morphing',
    license='Apache License, Version 2.0',
    url='https://github.com/avojak/image-morphing',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    zip_safe=False,
    include_package_data=True,
    packages=['webmorphing']
)