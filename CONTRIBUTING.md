# Contributing to peepDB

We're thrilled that you're interested in contributing to peepDB! This document provides guidelines for contributing to the project. Please take a moment to review this document to make the contribution process easy and effective for everyone involved.

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct (to be added).

## Getting Started

1. Fork the repository on GitHub.
2. Clone your fork locally:
   ```
   git clone https://github.com/evangelosmeklis/peepdb.git
   cd peepdb
   ```
3. Create a branch for your feature or bug fix:
   ```
   git checkout -b feature/your-feature-name
   ```
4. Make your changes and commit them with a clear commit message.
5. Push your changes to your fork:
   ```
   git push origin feature/your-feature-name
   ```
6. Create a pull request from your fork to the main peepDB repository.

## Setting Up Development Environment

1. Ensure you have Python 3.6 or higher installed.
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the package in editable mode with development dependencies:
   ```
   pip install -e .[dev]
   ```
4. Database Setup: Set up a test database (MySQL, PostgreSQL, etc.) locally or use Docker


## Running Tests

We use pytest for our test suite. To run the tests:

```
pytest
```

Please ensure all tests pass before submitting a pull request.

## Coding Standards

- Follow PEP 8 guidelines for Python code.
- Use meaningful variable and function names.
- Write docstrings for all functions, classes, and modules.
- Keep lines to a maximum of 100 characters.
- Use type hints where appropriate.

## Pull Request Process

1. Ensure your code adheres to the coding standards outlined above.
2. Update the README.md with details of changes to the interface, if applicable.
3. Add or update tests as necessary.
4. Update the documentation to reflect any changes.
5. Ensure all tests are passing.
6. Your pull request will be reviewed by maintainers, who may request changes or provide feedback.

## Reporting Bugs

1. Check the GitHub Issues to see if the bug has already been reported.
2. If not, create a new issue, providing as much detail as possible:
   - A clear, descriptive title
   - A detailed description of the issue
   - Steps to reproduce the problem
   - Expected behavior
   - Actual behavior
   - Your environment (OS, Python version, peepDB version, etc.)

## Suggesting Enhancements

We welcome suggestions for enhancements! Please create an issue on GitHub with the tag "enhancement" and provide:

- A clear, descriptive title
- A detailed description of the proposed enhancement
- Any potential implementation deta
