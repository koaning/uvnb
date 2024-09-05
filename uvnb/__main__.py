import click
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import subprocess
import tomllib
import re
from typing import Dict, Optional, Any

def parse_inline_metadata(script_content: str) -> Optional[Dict[str, Any]]:
    """
    Parse inline metadata from a Python script.

    The metadata should be at the top of the file in the following format:
    # /// script
    # requires-python = ">=3.11"
    # dependencies = [
    #   "requests<3",
    #   "rich",
    # ]
    # ///

    Args:
        script_content (str): The content of the Python script.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing the metadata,
                                  or None if no metadata is found.
    """
    metadata_pattern = r'^# /// script\n((?:# .*\n)+)# ///'
    match = re.search(metadata_pattern, script_content, re.MULTILINE)
    
    if not match:
        return None
    
    metadata_lines = match.group(1).strip().split('\n')
    metadata = {}
    
    # Join the metadata lines into a single string and parse it as TOML
    toml_string = '\n'.join(line.lstrip('# ') for line in metadata_lines)
    parsed_toml = tomllib.loads(toml_string)
    
    # Extract the required information from the parsed TOML
    if 'requires-python' in parsed_toml:
        metadata['python_version'] = parsed_toml['requires-python']
    if 'dependencies' in parsed_toml:
        metadata['dependencies'] = parsed_toml['dependencies']
    return metadata


@click.group()
def cli():
    """CLI for working with Jupyter notebooks."""
    pass

@cli.command()
@click.argument('notebook_path', type=click.Path(exists=True))
@click.option('--output-path', '-o', type=click.Path(), help='Path to save the executed notebook')
def run(notebook_path, output_path):
    """Run a Jupyter notebook."""
    
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)
    
    metadata = parse_inline_metadata(nb.cells[0].source)

    print(metadata)
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    parsed_deps = ["nbconvert", "jupyterlab"] + metadata.get('dependencies', [])
    with_deps = []
    for dep in parsed_deps:
        with_deps.append("--with")
        with_deps.append(dep)
    cmd = ["uv", "run"] + with_deps + ["jupyter", "nbconvert", "--to", "html", "--execute"]
    if output_path:
        cmd.append("--output")
        cmd.append(output_path)
    cmd.append(notebook_path)
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)


@cli.command()
@click.argument('notebook_path', type=click.Path(exists=True))
@click.option('--port', '-p', default=8888, help='Port to run Jupyter on')
@click.option('--no-browser', is_flag=True, help='Don\'t open a browser automatically')
def start(notebook_path, port, no_browser):
    """Start Jupyter notebook server."""
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)
    
    metadata = parse_inline_metadata(nb.cells[0].source)

    print(metadata)
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    parsed_deps = ["nbconvert", "jupyterlab"] + metadata.get('dependencies', [])
    with_deps = []
    for dep in parsed_deps:
        with_deps.append("--with")
        with_deps.append(dep)
    cmd = ["uv", "run"] + with_deps + ["jupyter", "lab", notebook_path, "--port", str(port)]
    if no_browser:
        cmd.append("--no-browser")
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)



if __name__ == '__main__':
    cli()