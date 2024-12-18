.PHONY: help makemigrations migrate build bash load up down dump createsuperuser reset shell

migrations:
	docker compose run -it src poetry run python manage.py makemigrations

migrate: makemigrations
	docker compose run -it src poetry run python manage.py migrate

build: migrate
	docker build -t src -f ops/src.Dockerfile ./src

bash:
	docker compose exec -it src bash

load:
	docker compose exec -it src poetry run python manage.py loaddata --exclude contenttypes /app/data.json

up:
	docker compose up $(if $(DETACH),-d) --build

down:
	docker compose down --remove-orphans --volumes

dump:
	docker compose exec -it src poetry run python manage.py dumpdata -o data.json
	docker cp netic-src-1:/app/data.json ./src/data.json

createsuperuser:
	docker compose run -it src poetry run python manage.py createsuperuser --noinput --username Admin --email netic_admin@eticalgarve.com
	docker compose exec -it src poetry run python manage.py shell -c "\
from django.contrib.auth import get_user_model; \
User = get_user_model(); \
user = User.objects.get(username='Admin'); \
user.set_password('Password'); \
user.save(); \
from app.models import UserProfile; \
UserProfile.objects.create(user=user, first_name='Admin', last_name='Admin', email='netic_admin@eticalgarve.com')"

urls:
	docker compose exec -it src poetry run python manage.py show_urls

setup:
	docker compose up -d
	make migrate
	make load

reset: 
	docker compose down
	docker compose up -d
	make migrate
	make load 

flush:
	docker compose exec -it src poetry run python manage.py flush --noinput

# De-comment the following line to update avatars in case DB needs to be reset
# make profilepictures:
# 	docker compose exec -it src poetry run python manage.py update_avatars