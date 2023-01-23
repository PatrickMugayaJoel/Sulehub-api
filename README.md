# Sulehub-api

Student-teacher Educational Application API

## Running the api

- Clone this repository
- Install python3.10
- Intall dependencies:
  > pip install -r requirements.txt
- Run the server:
  > python manage.py runserver

---

## Docker Setup

- Install [docker compose](https://docs.docker.com/compose/install/)
- Start the docker engine:

  > Create a 'master_app.log' file in the root directory.
  > Create a '.env' file with the necessary values (see env_example file).
  > RUN: docker-compose build
  > RUN: docker-compose up

- To check the server, open `http://localhost:8000/`
