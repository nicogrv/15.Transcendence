
COMPOSE_FILE = docker-compose.yml
DC = docker compose

all: build up
build:
	$(DC) -f $(COMPOSE_FILE) build
up:
	$(DC) -f $(COMPOSE_FILE) up 

backend:
	@ sudo docker exec -it backend bash

down:
	$(DC) -f $(COMPOSE_FILE) down

clean:
	@chmod +x ./tools/docker_clean.sh
	@./tools/docker_clean.sh

prune:
	@docker system prune --all --force --volumes

.PHONY: all build down clean prune backend