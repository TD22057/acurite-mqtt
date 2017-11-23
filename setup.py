#!/usr/bin/env python

from setuptools import setup

readme = open('README.md').read()
requirements = open("requirements.txt").readlines()
test_requirements = []

setup(
    name='acurite-mqtt',
    version='0.2.1',
    description="Acurite bridge output to MQTT",
    long_description=readme,
    author="Ted Drain",
    author_email='',
    url='https://github.com/TD22057/project',
    packages=['acurite_mqtt'],
    scripts=['scripts/acurite-mqtt.py'],
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    # avoid eggs
    zip_safe=False,
)
