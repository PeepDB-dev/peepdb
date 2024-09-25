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

- Python 3.9 or higher
- pip (Python package installer)

## System Dependencies

Before installing peepdb, ensure you have the following system dependencies:

For Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install libmariadb3 libmariadb-dev
```

For macOS (using Homebrew):
```bash
brew install mariadb
```

For Windows:
The necessary dependencies should be automatically installed with the Python package. If you encounter any issues, please refer to the troubleshooting section below.

## Verifying the Installation

After installation, you can verify that peepDB is installed correctly by running:

```bash
peepdb --version
```

This should display the version number of peepDB installed on your system.

## Troubleshooting

### Windows Users

If you encounter an error like "The term 'peepdb' is not recognized as the name of a cmdlet", you may need to add the Python Scripts folder to your PATH. Here's how:

1. Find the Python Scripts folder (usually `C:\Users\YourUsername\AppData\Local\Programs\Python\PythonXX\Scripts`)
2. Add this path to your system's PATH environment variable
3. Restart your command prompt and try running `peepdb --version` again

### Linux/macOS Users

If you encounter permission errors when installing, you may need to use `sudo`:

```bash
sudo pip install peepdb
```

Alternatively, you can install peepDB for your user only:

```bash
pip install --user peepdb
```

If you use the `--user` option, make sure your user's bin directory is in your PATH.

## Next Steps

Once you have peepDB installed, you can proceed to the [Usage](usage.md) page to learn how to use the tool effectively.
