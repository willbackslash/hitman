# Hitman API

## Quick start

### Running the project
> make up

Go to http://localhost/docs
### Seeing the logs
> make logs
### Running the code lintern (black)
> make lint
### Make migrations
> make migrations
### Migrate
> make migrate
### Running the tests
> make test
### Running only the db
> make up-db
### Stopping and removing containers
> make down

## Docs
### Swagger
http://localhost/docs
### Redoc
http://localhost/redoc

## For native development with virtualenv
Start only the db
> make up-db
### Install dependencies
> pip install poetry

> poetry install

> poetry shell
### Set env variables
> set -a && source .env
### Add local-db to your /etc/host
> sudo bash -c "echo '127.0.0.1 local-db' >> /etc/hosts"
### Run the app
> python manage.py runserver
### Try it
Go to http://localhost:8000/docs

## Swagger Docs Authentication

You can use the /auth/token endpoint to generate tokens or you can login to swagger using basic auth (email, password)
