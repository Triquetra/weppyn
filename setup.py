#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import find_packages
from setuptools import setup

setup(
    name='weppyn',
    version='0.1.2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    install_requires=[
        'click',
        'weppy',
    ],
    entry_points={
        "console_scripts": [
            "weppyn = weppyn.cli:cli",
        ]
    },
)
