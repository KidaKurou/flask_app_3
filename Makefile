.PHONY: build test lint deploy

# Development
build:
	docker-compose build

run:
	docker-compose up

# Testing
test:
	docker-compose -f docker-compose.test.yml run test

test-local:
	pytest

test-cov:
	pytest --cov=app --cov-report=html

# Linting
lint:
	flake8 app tests
	black app tests --check
	isort app tests --check-only

format:
	black app tests
	isort app tests

# Deployment
deploy-prod:
	docker-compose -f docker-compose.prod.yml up -d

deploy-staging:
	docker-compose -f docker-compose.staging.yml up -d

# Database
db-migrate:
	flask db migrate

db-upgrade:
	flask db upgrade

# Clean up
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +