
For more information, see the official PEP8 documentation: https://peps.python.org/pep-0008/
# File Naming Convention for Data Science Workflow

This repository uses a structured file naming convention to ensure clarity, reproducibility, and traceability throughout the data science workflow. The convention is as follows:

```
PRJ_tsv#_xxxxxxxxxxxx_yyyy-mm-dd.ext
```

Where:
- **PRJ**: 3-5 character project mnemonic (fixed string)
- **_**: underscore separator
- **t**: task number (0-6, see below)
- **s**: step letter within task (a, b, c, ...)
- **#**: version number (1, 2, 3, ...)
- **_**: underscore separator
- **xxxxxxxxxxxx**: short description of the step (5-10 characters, use underscores or hyphens for spaces)
- **_**: underscore separator
- **.ext**: file extension (e.g., .py, .csv, .ipynb)

## Version Control
Version control is maintained by GitHub. Please see the GitHub Repo for past versions of files.

If GitHub is not used for version control please include a version number and date in the filename. Note - replace dashes with _ or remove if the file is uses as part of a python package.
- **v**: version indicator (v)
- **yyyy-mm-dd**: date (year, month, day)

## Example
```
ABC_1a_cleaning.py
```

## Data Science Workflow Task Numbers
- **0**: Research Log or Project Admin
- **1**: Obtain Data
- **2**: Clean Data
- **3**: Explore Data
- **4**: Model Data
- **5**: Interpret Data
- **6**: Publish Data

## Notes
- Keep the description concise and standardized.
- Use all lowercase for filenames to avoid OS compatibility issues.
- For Python package modules, use PEP8-compliant names (lowercase, underscores, no dashes or numbers at the start).
- This convention is especially useful for data files, scripts, and notebooks.
- This package has minimal files and uses simple, PEP8-compliant file names in the source folder.

### What is PEP8?
PEP8 is the Python Enhancement Proposal that defines the style guide for Python code. It recommends best practices for code layout, naming, and formatting to ensure readability and consistency across Python projects. PEP stands for "Python Enhancement Proposal." Following PEP8 means using lowercase letters, underscores instead of dashes, and avoiding numbers at the start of filenames for Python modules.

For more information, see the official PEP8 documentation: https://peps.python.org/pep-0008/

---

*Maintained by project admin. Last updated: 2025-09-23.*
