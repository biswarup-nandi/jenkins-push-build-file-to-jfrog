from setuptools import setup, find_packages

setup(
    name='dbx_api_project',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'dbx-utility = dbx_api_project.databricks_api:main',
        ],
    }
)
