# Setting Up a Python Environment in VS Code

You have two main options for creating a clean Python environment for development and testing in VS Code:

## Option 1: Using Anaconda (PowerShell or Anaconda Prompt)

1. Open Anaconda Prompt or PowerShell.
2. Create a new conda environment (replace `pypdfcodebook` and `3.12` with your preferred name and Python version):
	```sh
	conda create -n pypdfcodebook python=3.12
	conda activate pypdfcodebook
	```
3. Install required packages:
	```sh
	conda install numpy pandas seaborn matplotlib jupyter
	pip install build twine fpdf2
	```
4. In VS Code, select the new environment as your Python interpreter (Ctrl+Shift+P → "Python: Select Interpreter").

## Option 2: Using venv in the VS Code Terminal

1. Open the integrated terminal in VS Code (Ctrl+` or View → Terminal).
2. Create a new virtual environment in your project folder:
	```sh
	python -m venv .venv
	```
3. Activate the environment:
	- **PowerShell:**
	  ```sh
	  .\.venv\Scripts\Activate.ps1
	  ```
	- **Command Prompt:**
	  ```sh
	  .\.venv\Scripts\activate.bat
	  ```
	- **Bash (macOS/Linux):**
	  ```sh
	  source .venv/bin/activate
	  ```
4. Upgrade pip and install required packages:
	```sh
	python -m pip install --upgrade pip
	pip install numpy pandas seaborn matplotlib jupyter build twine fpdf2
	```
5. In VS Code, select the `.venv` environment as your Python interpreter (Ctrl+Shift+P → "Python: Select Interpreter").

**Best Practice:**
- Always activate your environment before running Python commands or installing packages.
- Use `.venv` as the folder name for easy auto-detection by VS Code.

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
------
## Virtual Environment Option

```sh
.\venv\Scripts\Activate.ps1
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

Before building, delete any old files in the `dist/` directory to avoid uploading duplicate versions. It's also important to remove any `.egg-info` folders, which store metadata from previous builds and can cause packaging or upload issues if stale:

```powershell
Remove-Item dist\* -Force
Remove-Item build\* -Recurse -Force
# Remove all .egg-info folders anywhere in the project (recursively)
Get-ChildItem -Path . -Filter *.egg-info -Recurse | Remove-Item -Recurse -Force
```

**Explanation:**
- `Remove-Item dist\* -Force` deletes all files in the `dist` folder (old build artifacts).
- `Remove-Item build\* -Recurse -Force` deletes all files and subfolders in the `build` directory (temporary build files).
- `Get-ChildItem -Path . -Filter *.egg-info -Recurse | Remove-Item -Recurse -Force` finds and deletes all `.egg-info` folders anywhere in your project tree, not just the top level. This ensures no stale metadata remains from previous builds, which can otherwise cause versioning or packaging errors.

**Why is this important?**
Stale `.egg-info` folders or old build artifacts can lead to:
- Incorrect or duplicate version uploads
- Packaging errors or warnings
- Confusion for users and tools about the current package state
Cleaning these before each build ensures a fresh, reliable package is created and uploaded.

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
After installing, open a Python interpreter 
```sh
python
```

and run:
```python
import pypdfcodebook
print(pypdfcodebook.__version__)
# Optionally, test a function:
from pypdfcodebook.simple import add_one
add_one(1)
from pypdfcodebook.pdfcb_03c_codebook import codebook
help(codebook.add_projectoverview)
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

# Installing Your Package in a Different Project

Once your package is uploaded to TestPyPI, you can install it in any other project or environment for testing. There are two main ways to do this:

## Option 1: Simple Install (TestPyPI Only)
This command installs your package from TestPyPI:
```sh
pip install -i https://test.pypi.org/simple/ pypdfcodebook
```
**Note:** This will only find dependencies that are also on TestPyPI. If your package depends on other packages that are not on TestPyPI, the install may fail.

## Option 2: Robust Install (TestPyPI + PyPI Fallback)
This command tells pip to look for your package on TestPyPI, but fetch any dependencies from the main PyPI if needed:
```sh
pip install --upgrade --no-cache-dir --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pypdfcodebook
```
- `--index-url` sets the primary index to TestPyPI (where your test package lives).
- `--extra-index-url` adds the main PyPI as a fallback for dependencies.
- `--no-cache-dir` ensures pip does not use cached wheels (helpful for repeated testing).

**Best Practices:**
- Always use a clean virtual environment or conda environment for testing installs.
- Uninstall any previous versions before installing a new one:
	```sh
	pip uninstall pypdfcodebook
	```
- After install, verify the version and basic functionality:
	```python
	import pypdfcodebook
	print(pypdfcodebook.__version__)
	```
- Remember: TestPyPI is public, but not indexed by default. Anyone with the correct pip command can install your package from TestPyPI.

**For production or sharing with others:**
- Only use TestPyPI for testing. For public release, upload to the main PyPI.
- If you need a private package, consider a private PyPI server or repository.
---
*Maintained by project admin. Last updated: 2025-09-25.*
