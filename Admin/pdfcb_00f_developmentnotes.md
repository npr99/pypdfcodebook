This might need to go into the testpypi guide... but 

I just learned that while I am developing the code I need to use

`pip install -e .`

`-e`: Stands for "editable" or "development" mode. This is the same as --editable

`.`: The dot represents the current directory where your package's setup.py or pyproject.toml is located

When you run `pip install -e .`, instead of copying your package files to the Python site-packages directory (like a normal install does), pip creates a special link (called an "editable installation") that points directly to your development code.

I was having consistent errors and could not figure out why they would not go away despite changing the code.

This issue is not clear to me - but I am going to try the `pip install -e .`