migrate:
	docker compose run -it src poetry run python manage.py makemigrations

build: migrate
	docker build -t src -f ops/src.Dockerfile ./src

bash:
	docker compose exec -it src bash

up:
	docker compose up --build

dump:
	docker compose exec -it src poetry run python manage.py dumpdata -o data.json
	docker cp django-postgres-src-1:/app/data.json ./data.json

load:
	docker compose exec -it src poetry run python manage.py loaddata /app/data.json