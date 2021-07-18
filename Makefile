.PHONY: lint test exapmle publish test_all

MODULE="dataclass_utils"
lint:
	autoflake --remove-all-unused-imports --in-place -r ${MODULE}
	isort ${MODULE}
	black ${MODULE}
	mypy ${MODULE}

test: run_example
	poetry run pytest

test_all:
	python test.py all

run_example:
	ls examples/*py | xargs poetry run python
	poetry run mypy dataclass_utils

publish: test_all lint
	git diff --exit-code # check working directory is clean
	poetry publish --build
