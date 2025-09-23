# How to Set Up and Use a `.pypirc` File for PyPI/TestPyPI

## What is `.pypirc`?
The `.pypirc` file is a configuration file used by Python packaging tools (like `twine`) to securely store your PyPI or TestPyPI credentials. It allows you to upload packages without entering your username and API token every time, making the process easier and more secure.

## Where to Create the `.pypirc` File
- Place the `.pypirc` file in your user home directory.

### On Windows
```
C:\Users\<your-username>\.pypirc
```

### On Mac OS or Linux
```
/Users/<your-username>/.pypirc
```

## Example `.pypirc` for TestPyPI
```ini
[distutils]
index-servers =
    testpypi

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-<your-token-here>
```
- Replace `<your-token-here>` with your actual API token from TestPyPI.
- Keep this file private and never commit it to version control.

## Why Use `.pypirc`?
- Saves your credentials for easy, secure package uploads.
- Avoids entering your token every time you use `twine upload`.
- Reduces the risk of exposing your token in command history or scripts.

---
*Maintained by project admin. Last updated: 2025-09-23.*
