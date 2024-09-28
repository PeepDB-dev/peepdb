from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="peepdb",
    version="0.1.4",
    author="Evangelos Meklis",
    author_email="vmeklis@hotmail.com",
    description="CLI tool to view database tables fast",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PeepDB-dev/peepdb",
    packages=find_packages(),
    install_requires=[
        "mysql-connector-python>=9.0.0",
        "psycopg2-binary>=2.9.9",
        "pymysql>=1.1.1",
        "cryptography>=43.0.0",
        "tabulate>=0.8.9",
        "click>=8.0.0",
        "mariadb",
        "cachetools>=5.5.0",
        "keyring>=25.4.1",
        "pymongo==4.9.1",
        "dnspython==2.6.1"
    ],
    extras_require={
        'dev': [
            'coverage>=7.6.1',
            'pytest>=8.3.2',
            'pytest-cov>=5.0.0',
        ],
        'system': ['libmariadb3', 'libmariadb-dev'],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "peepdb=peepdb.cli:main",
        ],
    },
)