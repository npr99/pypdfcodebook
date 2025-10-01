This might need to go into the testpypi guide... but 

I just learned that while I am developing the code I need to use

`pip install -e .`

`-e`: Stands for "editable" or "development" mode. This is the same as --editable

`.`: The dot represents the current directory where your package's setup.py or pyproject.toml is located

When you run `pip install -e .`, instead of copying your package files to the Python site-packages directory (like a normal install does), pip creates a special link (called an "editable installation") that points directly to your development code.

I was having consistent errors and could not figure out why they would not go away despite changing the code.

This issue is not clear to me - but I am going to try the `pip install -e .`

## Pytest Output Capturing

When running tests with pytest, print statements in your test code are captured by default and only shown if the test fails. This can make debugging difficult because you can't see the output of your print statements during development.

To see all print statements while running tests, use the `-s` flag (or `--capture=no`):

```bash
python -m pytest tests/test_codebook_with_images.py -v -s
```

Useful pytest flags:
- `-s`: Shows all print statements (disables output capturing)
- `-v`: Verbose mode, shows more details about which tests are running
- You can combine flags: `-v -s` for both verbose output and print statements

This is particularly helpful when debugging test failures or when you want to see the progress of long-running tests.