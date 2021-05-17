build:
	docker-compose -f docker-compose.yml build

up:
	docker-compose -f docker-compose.yml up

upd:
	docker-compose -f docker-compose.yml up -d

down:
	docker-compose -f docker-compose.yml down --remove-orphans

logs:
	docker-compose -f docker-compose.yml logs

build-dist:
	docker-compose -f docker-compose.prod.yml --rm run front
