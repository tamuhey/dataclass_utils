.PHONY: lint

MODULE="dataclass_utils"
lint:
	autoflake --remove-all-unused-imports --in-place -r ${MODULE}
	isort ${MODULE}
	black ${MODULE}
	mypy ${MODULE}

test: lint
	pytest

