try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import codecs
import os
import re
import sys


here = os.path.abspath(os.path.dirname(__file__))

py3 = sys.version_info[0] == 3


# Read the version number from a source file.
# Why read it, and not import?
# see https://groups.google.com/d/topic/pypa-dev/0PkjVpcxTzQ/discussion
def find_version(*file_paths):
    # Open in Latin-1 so that we avoid encoding errors.
    # Use codecs.open for Python 2 compatibility
    with codecs.open(os.path.join(here, *file_paths), 'r', 'latin1') as f:
        version_file = f.read()

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string')


def read_description(filename):
    with codecs.open(filename, encoding='utf-8') as f:
        return f.read()


install_requires = [
    'click>=3.3,<3.4',
    'lxml>=3.4.0,<3.5.0',
    'pycrypto>=2.6.1,<2.7.0',
    'requests>=2.5.0,<2.6.0',
]

dev_requires = [
    'ipython',
]

setup(
    name='twbanker',
    version=find_version('twbanker', '__init__.py'),
    url='https://github.com/eliangcs/twbanker',
    description='Show you the money in your Taiwan banks',
    long_description=read_description('README.rst'),
    author='Chang-Hung Liang',
    author_email='eliang.cs@gmail.com',
    license='MIT',
    packages=['twbanker', 'twbanker.banks'],
    install_requires=install_requires,
    extras_require={
        'dev': dev_requires
    },
    entry_points="""
        [console_scripts]
        twbanker=twbanker.cli:main
    """,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Office/Business :: Financial :: Accounting'
    ]
)
