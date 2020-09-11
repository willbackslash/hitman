# Save the docker exec command in a var
APP_SHELL = docker-compose exec app

# Bring up the needed env variables
include .env
export

up:
	@# It will start both local-db and app
	docker-compose up --build --detach

logs:
	docker-compose logs --follow

lint:
	@# Applies  standard code formatting to the project
	black --exclude db-data .

migrations:
	@# Checks for changes that would need new migrations
	python manage.py makemigrations

migrate:
	@# Checks for changes that would need new migrations
	python manage.py migrate