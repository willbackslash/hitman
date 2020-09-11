up:
	@# It will start both local-db and app
	docker-compose up --build --detach

logs:
	docker-compose logs --follow
