build:
	docker-compose -f docker-compose.yml build

up:
	docker-compose -f docker-compose.yml up

upd:
	docker-compose -f docker-compose.yml up -d

down:
	docker-compose -f docker-compose.yml down -v --remove-orphans

clean:
	docker-compose -f docker-compose.yml down -v --remove-orphans

logs:
	docker-compose -f docker-compose.yml logs --follow --tail=50

restart:
	make down && make upd && sleep 8 && make seed

seed:
	docker exec enki_api_1 flask create-position-groups
	docker exec enki_api_1 flask create-position-groups

shell:
	docker-compose exec enki-api flask shell

# Provisions

build-provision:
	docker-compose -f docker-compose.provision.yml build

run-provision:
	docker-compose -f docker-compose.provision.yml run --rm affairs-provision

# Tests

test-resource-up:
	docker-compose -f docker-compose.test.yml up

test-resource-down:
	docker-compose -f docker-compose.test.yml down -v --remove-orphans

# Migrations
create-migration:
	docker exec enki_api_1 alembic revision --autogenerate -m "test"
run-migration:
	docker exec enki_api_1 alembic upgrade head
stamp-migration:
	docker exec enki_api_1 alembic stamp head

