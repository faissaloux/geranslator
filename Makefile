NAME = geranslator

clean:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf *_cache
	rm -rf */__pycache__
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf .coverage

install: clean
	pip install -e ."[dev]"

test: clean
	pytest --cov -v

lint: mypy

mypy:
	mypy --show-error-codes $(NAME) tests

precommit: clean
	pre-commit run --all-files
