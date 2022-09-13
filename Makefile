.PHONY: tests_tox tests tests_integration tests_types create_requirements build
.DEFAULT_GOAL := tests

tests_tox:
	poetry run tox

tests:
	pytest tests

lint:
	poetry run black . --check
	poetry run flake8
	mypy bas_python_api/

lint_fix:
	poetry run black .

clean:
	rm -rf ./build || echo ""
	rm -rf ./.tox || echo ""
	rm -rf ./bas_remote_python.egg-info || echo ""
	rm -rf ./.bas-remote-app-* || echo ""
	rm -rf ./.pytest_cache || echo ""
	rm -rf ./.mypy_cache || echo ""
	rm -rf ./dist || echo ""

build:
	poetry build -f wheel -n
	poetry build -f sdist -n

upload_pypi:
	$(clean)
	$(build)
	twine upload dist/*.tar.gz dist/*.whl
