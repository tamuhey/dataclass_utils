.PHONY: lint test

MODULE="dataclass_utils"
lint:
	autoflake --remove-all-unused-imports --in-place -r ${MODULE}
	isort ${MODULE}
	black ${MODULE}
	mypy ${MODULE}

test:
	poetry run pytest
	poetry run python -m doctest README.md

