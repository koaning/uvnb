.PHONY: docs

install:
	uv venv 
	uv pip install -e ".[dev]" twine wheel

clean:
	rm -rf .pytest_cache
	rm -rf build
	rm -rf dist
	rm -rf .ipynb_checkpoints
	rm -rf .coverage*


pypi: clean
	python -m build
	python -m twine upload dist/*