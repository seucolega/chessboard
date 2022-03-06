.PHONY:	install format lint test
ISORT_ARGS=--trailing-comma --multi-line 3

install:
	@poetry install
format:
	@blue .
	@isort . $(ISORT_ARGS)
lint:
	@blue . --check
	@isort . --check $(ISORT_ARGS)
test:
	@prospector .
	@pytest . --cov
