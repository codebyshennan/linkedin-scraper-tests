.PHONY: test lint clean

test:
	pytest tests/ -v --cov=src

lint:
	flake8 src/ tests/
	black src/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name *.pyc -delete
	rm -rf .coverage htmlcov/