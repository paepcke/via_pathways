import multiprocessing
from setuptools import setup, find_packages
import os
import glob

datafiles = ['src/via_pathways/Data/graph.txt'
             ]

setup(
    name = "via_pathways",
    version = "0.1",
    packages = find_packages(),

    # Dependencies on other packages:
    # Couldn't get numpy install to work without
    # an out-of-band: sudo apt-get install python-dev
    setup_requires   = [],
    install_requires = ['click>=7.0',
                        'pandas>=0.23.4',
                        'numpy>=1.15.4',
                        ],

    # Unit tests; they are initiated via 'python setup.py test'
    test_suite       = 'nose.collector', 

    # metadata for upload to PyPI
    author = "Geoffrey Lim Angus, Richard Diehl Martinez",
    author_email = "paepcke@cs.stanford.edu",
    description = "Deriving course prerequisites from enrollment data..",
    license = "BSD",
    keywords = "education",
    url = "git@github.com:paepcke/via_pathways.git",   # project home page, if any
)
