.PHONY: docs

install:
	uv venv 
	uv pip install -e ".[dev]"

pypi: clean
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload dist/*