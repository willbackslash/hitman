# Save the docker exec command in a var
APP_SHELL = docker-compose exec app

# Bring up the needed env variables
include .env
export

up:
	@# It will start both local-db and app
	test -f .env || cp .env.dist .env
	docker-compose up --build --detach

up-db:
	@# It will start only local-db
	docker-compose up --detach local-db

logs:
	docker-compose logs --follow

lint:
	@# Applies  standard code formatting to the project
	black --exclude db-data --exclude venv .

migrations:
	@# Checks for changes that would need new migrations
	python manage.py makemigrations

migrate:
	@# Checks for changes that would need new migrations
	python manage.py migrate

test:
	@ # Run the test cases
	python manage.py test

down:
	@ #remove all the containers
	docker-compose stop
	docker-compose rm --force
