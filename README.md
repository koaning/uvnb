<img src="img.png" width="125" height="125" align="right" />

### uvnb

> Have UV deal with all your Jupyter deps.

## Quickstart 

You can install this tool via: 

```
uv pip install uvnb
```

## Usage 

The goal of `uvnb` is to allow you to run Jupyter notebooks with dependencies via UV by leveraging the script metadata. By doing this, you can just define your dependencies in the notebook as a metadata comment and quickly run it. 

This tool assumes that you have metadata in the first cell, maybe something that looks like this: 

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

To learn more about this syntax, you can check [this PEP](https://packaging.python.org/en/latest/specifications/inline-script-metadata/). From here you can run the notebook, or start a Jupyter server via the command line. 

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

## UV to the max 

Fun fact, you don't have to install this tool beforehand. You can just run it with `uv`: 

```
uv run --with uvnb python -m uvnb
```

