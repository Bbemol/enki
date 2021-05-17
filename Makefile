setup:
	docker network create --driver=bridge enki_default

run-app:
	docker-compose -f docker-compose.app.yml up -d --force-recreate

run-gateway:
	docker-compose -f docker-compose.gateway.yml up -d --force-recreate

setup-gateway:
	docker-compose -f docker-compose.gateway.yml run --rm kong kong migrations bootstrap

run-auth:
	docker-compose -f docker-compose.auth.yml up -d --force-recreate


setup-app-dev:
	docker-compose -f docker-compose.app.dev.yml up -d postgres

run-app-dev:
	docker-compose -f docker-compose.app.dev.yml up -d

run-auth-dev:
	docker-compose -f docker-compose.auth.dev.yml up -d --force-recreate

setup-gateway-dev:
	docker-compose -f docker-compose.gateway.dev.yml up -d kong-db
	docker-compose -f docker-compose.gateway.dev.yml run --rm kong kong migrations bootstrap

run-gateway-dev:
	docker-compose -f docker-compose.gateway.dev.yml up -d

provision-dev:
	docker-compose -f docker-compose.provision.yml build keycloak-provision
	docker-compose -f docker-compose.provision.yml run --rm keycloak-provision
	docker-compose -f docker-compose.provision.yml build kong-provision
	docker-compose -f docker-compose.provision.yml run --rm kong-provision