install:
	poetry install

run:
	python3 manage.py runserver

migration:
	python3 manage.py makemigrations

migrate:
	python3 manage.py migrate

superuser:
	python3 manage.py createsuperuser

test:
	poetry run python manage.py test

lint:
	poetry run flake8

test-coverage:
	poetry run coverage run --source='.' manage.py test
	poetry run coverage report
	poetry run coverage xml