.PHONY:	install start user format lint test
ISORT_ARGS=--trailing-comma --multi-line 3

install:
	@poetry install
	@poetry run python manage.py collectstatic --noinput
	@poetry run python manage.py migrate
start:
	@poetry run python manage.py runserver
user:
	@poetry run python manage.py createsuperuser
format:
	@blue .
	@isort . $(ISORT_ARGS)
lint:
	@blue . --check
	@isort . --check $(ISORT_ARGS)
test:
	@prospector .
	@pytest . --cov
