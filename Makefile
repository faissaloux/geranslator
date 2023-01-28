NAME = geranslator
PYTHON = python3

clean:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf *_cache
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf .coverage
	find $(NAME) tests -type d -name '__pycache__' -exec rm -rf {} +

install: clean
	pip install -e ."[dev]"

build: clean
	$(PYTHON) setup.py bdist_wheel

test: clean
	pytest --cov -v

lint: mypy

mypy:
	mypy --show-error-codes $(NAME) tests

precommit: clean
	pre-commit run --all-files
