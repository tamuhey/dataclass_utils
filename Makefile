.PHONY: lint test exapmle

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
	git diff --exit-code || echo "\ncommit changes before publishing!!!\n" && exit 1
	poetry run pytest test
	poetry publish --build
