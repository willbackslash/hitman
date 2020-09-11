up:
	@# It will start both local-db and app
	docker-compose up --build --detach

logs:
	docker-compose logs --follow

lint:
	@# Applies  standard code formatting to the project
	black --exclude db-data .