.PHONY: tests_tox tests tests_multi tests_coverage lint lint_fix clean build
.DEFAULT_GOAL := tests

tests_tox:
	poetry run tox

tests:
	poetry run pytest tests/

tests_multi:
	poetry run pytest -n auto tests/

tests_coverage_multi:
	poetry run pytest -n auto --cov-report html --cov=bas_client tests/ &&	start "./htmlcov/index.html"

lint:
	poetry run black . --check
	poetry run flake8
	mypy bas_client/

lint_fix:
	isort bas_client/ tests/ tools/
	poetry run black .

clean:
	rm -rf ./.pytest_cache || echo ""
	rm -rf ./.tox || echo ""
	rm -rf ./htmlcov || echo ""
	rm .coverage || echo ""
	rm -rf ./dist || echo ""
	rm -rf ./tests/.tests_data || echo ""
	rm -rf ./tests/functional/.pytest_cache || echo ""
	rm -rf ./tests/unit/.pytest_cache || echo ""
	rm -rf ./tools/.tools_data || echo ""

build:
	poetry build -f wheel -n
	poetry build -f sdist -n

bump_version:
	poetry version patch

upload_pypi:
	$(clean)
	$(build)
	twine upload dist/*.tar.gz dist/*.whl
