from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="peepDB",
    version="0.1.0",
    author="Evangelos Meklis",
    author_email="vmeklis@hotmail.com",
    description="A quick database table viewer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/evangelosmeklis/peepDB",
    packages=find_packages(),
    install_requires=[
        "mysql-connector-python",
        "psycopg2-binary",
        "pymysql",
        "cryptography",
        "tabulate",
    ],
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