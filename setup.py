import os
import io

from setuptools import setup

PROJECT_ROOT, _ = os.path.split(__file__)

NAME = 'python-lightblue'
EMAILS = 'araszka@redhat.com, mbirger@redhat.com'
AUTHORS = 'Ales Raszka, Mark Birger'
VERSION = '1.0.2'

URL = 'https://github.com/redhat-aqe/python-lightblue'
LICENSE = 'GPLv3'


SHORT_DESCRIPTION = 'A Python API for Lightblue database.'

with io.open(os.path.join(PROJECT_ROOT, 'README.md'), encoding="utf-8") as f:
    DESCRIPTION = f.read()

INSTALL_REQUIRES = open(os.path.join(PROJECT_ROOT, 'requirements.txt')). \
        read().splitlines()
TEST_REQUIRES = open(os.path.join(PROJECT_ROOT, 'build_requirements.txt')). \
        read().splitlines()

setup(
    name=NAME,
    version=VERSION,
    author=AUTHORS,
    author_email=EMAILS,
    package_dir={'': 'src'},
    packages=[
        'lightblue',
        ],
    install_requires=INSTALL_REQUIRES,
    test_suite='nose.collector',
    tests_require=TEST_REQUIRES,
    url=URL,
    description=SHORT_DESCRIPTION,
    long_description=DESCRIPTION,
    long_description_content_type='text/markdown',
    license=LICENSE,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
