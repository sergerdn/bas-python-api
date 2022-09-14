.PHONY: tests_tox tests tests_integration tests_types create_requirements build
.DEFAULT_GOAL := tests

tests_tox:
	poetry run tox

tests:
	poetry run pytest

tests_coverage:
	poetry run pytest --cov-report html --cov=bas_api tests/
	start "./htmlcov/index.html"

lint:
	poetry run black . --check
	poetry run flake8
	mypy bas_api/

lint_fix:
	isort bas_api/ tests/
	poetry run black .

clean:
	rm -rf ./tests/.tests_data || echo ""
	rm -rf ./tests/functional/.pytest_cache || echo ""

poetry_upgrade:
	poetryup

build:
	poetry build -f wheel -n
	poetry build -f sdist -n

upload_pypi:
	$(clean)
	$(build)
	twine upload dist/*.tar.gz dist/*.whl
