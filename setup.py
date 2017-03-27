# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages

from dist_utils import fetch_requirements

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REQUIREMENTS_FILE = os.path.join(BASE_DIR, 'requirements.txt')

install_reqs, dep_links = fetch_requirements(REQUIREMENTS_FILE)

setup(
    name='yolo',
    version='0.0.1',
    description='Example Flask application',
    author='Chris Proto',
    author_email='cproto@sympoz.com',
    packages=[
        'yolo',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_reqs,
    dependency_links=dep_links
)
