.PHONY: init

init:
	make down
	make up
	make ps
	make migrate
down:
	docker-compose down --volumes --remove-orphans
pull:
	docker-compose pull
build:
	docker-compose build
up: pull build
	docker-compose up -d
ps:
	docker-compose ps
migrations:
	docker-compose run --rm core python manage.py makemigrations
migrate:
	make migrations
	docker-compose run --rm core python manage.py migrate
su:
	docker-compose run --rm core python manage.py createsuperuser
test:
	docker-compose run --rm core python manage.py test
shell:
	docker-compose run --rm core python manage.py shell
format:
	docker-compose run --rm core black .
lint:
	docker-compose run --rm core black . --check
setup:
	docker-compose run --rm core pre-commit install
prune:
	make down
	docker volume prune -f
	docker system prune -f
populatedb:
	docker-compose run --rm core python manage.py populatedb
