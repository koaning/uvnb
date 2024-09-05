<img src="img.png" width="125" height="125" align="right" />

### uvnb

> A utility to run UV against Jupyter notebooks.

## Quickstart 

You can install this tool via: 

```
uv pip install uvnb
```

## Usage 

The goal of `uvnb` is to allow you to run Jupyter notebooks with dependencies via UV by leveraging the script metadata. By doing this, you can just define your dependencies in the notebook metadata and quickly run it. 

This tool assumes that you have metadata in the first cell that looks like this: 

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests<3",
#   "rich",
# ]
# ///

import requests
from rich.pretty import pprint

resp = requests.get("https://peps.python.org/api/peps.json")
data = resp.json()
pprint([(k, v["title"]) for k, v in data.items()][:10])
```

From here you can run the notebook, or start a Jupyter server via the command line. 

```
python -m uvnb
Usage: python -m uvnb [OPTIONS] COMMAND [ARGS]...

  CLI for working with Jupyter notebooks.

Options:
  --help  Show this message and exit.

Commands:
  run    Run a Jupyter notebook.
  start  Start Jupyter notebook server.
```
