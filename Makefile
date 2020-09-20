up:
	@# It will start both frontend and backend
	docker-compose -f ./hitman-api/docker-compose.yml up --build --detach
	# docker-compose -f ./hitman-api/docker-compose.yml exec app python manage.py collectstatic --no-input
	docker-compose -f ./hitman-api/docker-compose.yml up --build --detach
	docker-compose -f ./hitman-ui/docker-compose.yml up --build --detach

down:
	# It will remove both frontend and backend
	docker-compose -f ./hitman-api/docker-compose.yml stop
	docker-compose -f ./hitman-api/docker-compose.yml rm
	docker-compose -f ./hitman-ui/docker-compose.yml stop
	docker-compose -f ./hitman-ui/docker-compose.yml rm

logs:
	docker-compose -f ./hitman-api/docker-compose.yml -f hitman-ui/docker-compose.yml logs --follow