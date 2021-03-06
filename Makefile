install:
	poetry install

test:
	poetry run pytest task_manager

test-coverage:
	poetry run pytest --cov=task_manager --cov-report xml

lint:
	poetry run flake8 task_manager

selfcheck:
	poetry check

check: selfcheck test-coverage lint

build:
	poetry build
	
package-install:
	pip install --user dist/*.whl

.PHONY: install test lint selfcheck check build
