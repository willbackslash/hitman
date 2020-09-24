# Hitman
## Stack
- API: Django + Django Rest Framework
- UI: React + React Bootstrap

## Structure
This project has the monorepo structure, you can find the backend project in `hitman-api` and the front-end in `hitman-ui`

## Pre-requirements
- Docker
- Docker-Compose
- Be sure that you have free ports 
    - `80` for API
    - `3000` for front-end
    - `5432` for postgres db

## Quick start
This quick start guide was only tested on mac os and linux. It won't work on windows
### Running backend and frontend together
From the hitman root directory
```console
make up
```

To see the logs:
```console
make logs
```

Go to http://localhost:3000

### Running only the backend (API)
> cd hitman-api  
> make up  

You can see the api docs in:  
Swagger: http://localhost/docs  
Redoc: http://localhost/redoc  

### Running only the frontend (UI) in development mode
```console
cd hitman-ui  
npm ci  
npm run start
```

Go to http://localhost:3000

### Running only the frontend with docker
```console
cd hitman-ui  
docker-compose up --build --detach
```

Go to http://localhost:3000

### Removig all the hitman containers
From the hitman root directory
```console
make down
```
---
### You can get more details in the README inside `hitman-api` or `hitman-ui`
---
## Initial users
All the users have the default password: `hitman2020`

### The users have the following hierarchy:
    theboss@hitman.com
    ├── manager1@hitman.com
    │   ├── hitman1@hitman.com
    │   ├── hitman2@hitman.com
    │   └── hitman3@hitman.com
    ├── manager2@hitman.com
    │   ├── hitman4@hitman.com
    │   ├── hitman5@hitman.com
    │   └── hitman6@hitman.com
    └── manager3@hitman.com
        ├── hitman7@hitman.com
        ├── hitman8@hitman.com
        └── hitman9@hitman.com
