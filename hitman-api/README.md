# Hitman API

## Quick start

### Running the project
```console
make up
```

Go to http://localhost/docs
### Seeing the logs
```console
make logs
```
### Running the code lintern (black)
```console
make lint
```
### Make migrations
```console
make migrations
```
### Migrate
```console
make migrate
```
### Running the tests
```console
make test
```
### Running only the db
```console
make up-db
```
### Stopping and removing containers
```console
make down
```

## Docs
### Swagger
http://localhost/docs
### Redoc
http://localhost/redoc

## For native development with virtualenv
Start only the db
```console
make up-db
```
### Install dependencies
```console
pip install poetry
poetry install
poetry shell
```
### Set env variables
```console
set -a && source .env
```
### Add local-db to your /etc/host
```console
sudo bash -c "echo '127.0.0.1 local-db' >> /etc/hosts"
```
### Run the app
```console
python manage.py runserver
```
### Try it
Go to http://localhost:8000/docs

## Swagger Docs Authentication

You can use the /auth/token endpoint to generate tokens or you can login to swagger using basic auth (email, password)
