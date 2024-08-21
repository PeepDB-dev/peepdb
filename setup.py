from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
try:
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ''

setup(
    name="peepDB",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "mysql-connector-python",
        "psycopg2-binary",
        "pymysql",
        "cryptography",
    ],
    entry_points={
        "console_scripts": [
            "peepdb=peepdb.cli:main",
        ],
    },
    author="Evangelos Meklis",
    author_email="vmeklis@hotmail.com",
    description="A quick database table viewer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/evangelosmeklis/peepDB",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)