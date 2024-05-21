from setuptools import setup, find_packages

setup(
    name='dbx-api-project',
    version='0.1.0',
    packages=find_packages(),
    python_requires='==3.12.3',
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'dbx-utility = dbx_api_project.databricks_api:main',
        ],
    },
)
