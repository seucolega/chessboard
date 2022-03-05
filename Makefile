.PHONY:	install format lint test
ISORT_ARGS=--trailing-comma --multi-line 3
PYTHONPATH=./chessboard

install:
	@cd $(PYTHONPATH) && poetry install
format:
	@cd $(PYTHONPATH) && blue .
	@cd $(PYTHONPATH) && isort . $(ISORT_ARGS)
lint:
	@cd $(PYTHONPATH) && blue . --check
	@cd $(PYTHONPATH) && isort . --check $(ISORT_ARGS)
test:
	@cd $(PYTHONPATH) && prospector .
	@cd $(PYTHONPATH) && pytest -v --cov --cov-report term-missing
