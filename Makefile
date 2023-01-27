NAME = geranslator

clean:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf *_cache
	rm -rf __pycache__
	rm -rf .coverage
	find . -type d -name "*_cache*" -exec rm -rf "{}" \;

install: clean
	pip install -e ."[dev]"

test: clean
	pytest --cov -v

mypy: clean
	mypy --show-error-codes $(NAME) tests
