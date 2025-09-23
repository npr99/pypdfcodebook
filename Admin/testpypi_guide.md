# TestPyPI Publishing & Installation Guide

This guide walks you through creating a clean environment, building, uploading, and testing your Python package on TestPyPI using conda and pip.

## 1. Remove Old Environment (if needed)
```sh
conda remove -n pypdfcodebook --all
```

## 2. Create a New Environment
```sh
conda create -n pypdfcodebook python=3.12
conda activate pypdfcodebook
```

## 2a. (Recommended) Upgrade pip
```sh
python -m pip install --upgrade pip
```

## 3. Install Core Packages with Conda
```sh
conda install numpy pandas seaborn
```

## 4. Install Other Useful Packages
```sh
conda install matplotlib jupyter
```

## 5. Install Build Tools with pip
```sh
pip install build twine fpdf2
```

## 6. Clean Old Builds (Recommended)
Before building, delete any old files in the `dist/` directory to avoid uploading duplicate versions:
```powershell
Remove-Item dist\* -Force
Remove-Item build\* -Recurse -Force
```

### CHECK VERSION
- Before uploading, increment the version number in both `pyproject.toml` (under `[project] version`) and the `__version__` variable in `src/pypdfcodebook/__init__.py` (each upload to TestPyPI must have a unique version).
- These two version numbers must always match for consistency and to avoid confusion for users and tools.

### CHECK API KEY
- Log into https://test.pypi.org/ (note will need to get authentication code from DUO)
- Under: https://test.pypi.org/manage/account/ scroll down to API tokens
- Make sure your `.pypirc` file is set up with your TestPyPI token. See [pypirc_instructions.md](pypirc_instructions.md) for setup details.

## 7. Build Your Package
```sh
python -m build
```

_NOTE_: Check that the version in the terminal output (e.g., `Successfully built pypdfcodebook-0.3.1.tar.gz`) matches the version set in both `pyproject.toml` and `src/pypdfcodebook/__init__.py`.

## 8. Upload to TestPyPI
```sh
twine upload --repository testpypi dist/*
```

## 9. Test Install from TestPyPI
If you are re-installing in an existing environment, uninstall first:
```sh
pip uninstall pypdfcodebook
```
Then install the latest version (using --no-cache-dir to avoid pip cache issues):
```sh
pip install --upgrade --no-cache-dir --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pypdfcodebook
```
If you do not get the expected version, try again after a few minutes or check the [TestPyPI project page](https://test.pypi.org/project/pypdfcodebook/) to verify the upload.


## 10. Test the Installed Package in Python
After installing, open a Python interpreter and run:
```python
import pypdfcodebook
print(pypdfcodebook.__version__)
# Optionally, test a function:
from pypdfcodebook.simple import add_one
add_one(1)
from pypdfcodebook.pdfcb_03a_figures import county_list_for_datacensusgov
help(county_list_for_datacensusgov)
exit()
```
If you see the version number and no errors, the install was successful.


## 11. (Optional) Run Tests
If you have a test suite, first install pytest (if not already installed):
```sh
pip install pytest
```
Then run:
```sh
pytest
```


## Notes
- Always specify dependencies in `pyproject.toml` for your users.
- Use conda for your own environment setup for best performance with scientific packages.
- If you want to provide a ready-to-use conda environment, consider creating an `environment.yml` file.
- Never commit your `.pypirc` file or API tokens to version control. Keep them in your home directory and add `.pypirc` to your `.gitignore` if needed.
- For more help, see the [TestPyPI documentation](https://test.pypi.org/help/).

---
*Maintained by project admin. Last updated: 2025-09-23.*
