from setuptools import setup, find_packages

import sys
sys.path.append('./wheel')

import datetime
import dbx_api_project

setup(
    name="dbx_api_project",
    version=dbx_api_project.__version__ + "+" + datetime.datetime.utcnow().strftime("%Y%m%d.%H%M%S"),
    url="https://databricks.com",
    author="biswarup.nandi@outlook.com",
    description="wheel file for dbx automation",
    packages=find_packages(where='./wheel'),
    package_dir={'': 'wheel'},
    entry_points={
        "packages": [
            "main=dbx_api_project.main:main"
        ]
    },
    install_requires=[
        "setuptools",
        "requests"
    ],
)