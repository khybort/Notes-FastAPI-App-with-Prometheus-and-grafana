.PHONY: debug up stop build

DOCKER_TODO=fast-api-example-web-1

build:
	docker-compose build

stop:
	docker-compose stop

debug:
	docker attach $(DOCKER_TODO)

up:
	docker-compose up -d