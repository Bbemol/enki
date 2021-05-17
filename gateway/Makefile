build:
	docker-compose -f docker-compose.yml build

build-provision:
	docker-compose -f docker-compose.provision.yml build

build-provision-prod:
	docker-compose -f docker-compose.prod.provision.yml build

setup:
	docker-compose -f docker-compose.yml up -d kong-db
	sleep 10
	docker-compose -f docker-compose.yml run --rm kong kong migrations bootstrap
	sleep 15
	docker-compose -f docker-compose.yml up -d kong

setup-prod:
	docker-compose -f docker-compose.prod.yml up -d kong-db
	sleep 10
	docker-compose -f docker-compose.prod.yml run --rm kong kong migrations bootstrap
	sleep 15
	docker-compose -f docker-compose.prod.yml up -d kong

provision:
	docker-compose -f docker-compose.provision.yml run --rm kong-provision
provision-prod:
	docker-compose -f docker-compose.prod.provision.yml run --rm kong-provision

up:
	docker-compose -f docker-compose.yml up

upd:
	docker-compose -f docker-compose.yml up -d

upd-prod:
	docker-compose -f docker-compose.prod.yml up -d

down:
	docker-compose -f docker-compose.yml down --remove-orphans -v
down-prod:
	docker-compose -f docker-compose.prod.yml down --remove-orphans -v

logs:
	docker-compose -f docker-compose.yml logs --follow

logs-prod:
	docker-compose -f docker-compose.prod.yml logs --follow