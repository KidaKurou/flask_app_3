.PHONY: test test-cov test-html lint

test:
	pytest

test-cov:
	pytest --cov=app --cov-report=term-missing

test-html:
	pytest --cov=app --cov-report=html

lint:
	flake8 app tests
	black app tests --check
	isort app tests --check-only