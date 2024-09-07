---
title: Installation
layout: default
---

# 📦 Installation

You can install peepDB directly from PyPI using pip:

```bash
pip install peepdb
```

This will install the latest version of peepDB along with all its dependencies.

## Requirements

- Python 3.6 or higher
- pip (Python package installer)

## System Dependencies

Before installing peepdb, ensure you have the following system dependencies:

```bash
sudo apt-get update
sudo apt-get install libmariadb3 libmariadb-dev
```

## Verifying the Installation

After installation, you can verify that peepDB is installed correctly by running:

```bash
peepdb --version
```

This should display the version number of peepDB installed on your system.

> **Note:** If peepdb gives an error like "The term 'peepdb' is not recognized as the name of a cmdlet" remember to add the Python Scripts folder to your PATH in Windows.

## Next Steps

Once you have peepDB installed, you can proceed to the [Usage](usage.md) page to learn how to use the tool effectively.
