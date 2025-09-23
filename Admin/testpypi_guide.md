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
```

## 7. Build Your Package
```sh
python -m build
```

## 8. Upload to TestPyPI
```sh
twine upload --repository testpypi dist/*
```
- Before uploading, increment the version number in the `__version__` variable in `src/pypdfcodebook/__init__.py` (each upload to TestPyPI must have a unique version).
- The version in `pyproject.toml` is now set automatically from your code, so you only need to update it in one place.
- Make sure your `.pypirc` file is set up with your TestPyPI token. See [pypirc_instructions.md](pypirc_instructions.md) for setup details.


## 9. Test Install from TestPyPI
```sh
pip install --upgrade --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pypdfcodebook
```

## 10. Test the Installed Package in Python
After installing, open a Python interpreter and run:
```python
import pypdfcodebook
print(pypdfcodebook.__version__)
# Optionally, test a function:
# pypdfcodebook.add_one(1)
exit()
```
If you see the version number and no errors, the install was successful.

## Notes
- Always specify dependencies in `pyproject.toml` for your users.
- Use conda for your own environment setup for best performance with scientific packages.
- If you want to provide a ready-to-use conda environment, consider creating an `environment.yml` file.

---
*Maintained by project admin. Last updated: 2025-09-23.*
