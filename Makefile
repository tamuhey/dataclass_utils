.PHONY: lint test exapmle publish

MODULE="dataclass_utils"
lint:
	autoflake --remove-all-unused-imports --in-place -r ${MODULE}
	isort ${MODULE}
	black ${MODULE}
	mypy ${MODULE}

test: run_example
	poetry run pytest

run_example:
	ls examples/*py | xargs poetry run python
	poetry run mypy dataclass_utils

publish: lint test
	git diff --exit-code # check working directory is clean
	poetry publish --build
