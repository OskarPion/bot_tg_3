COMPOSE_FILES = -f docker-compose.yaml

restart:
	docker compose restart bot
kill:
	sudo docker compose $(COMPOSE_FILES) kill

down:
	sudo docker compose $(COMPOSE_FILES) down
up:
	sudo docker compose $(COMPOSE_FILES) up -d

build:
	sudo docker compose $(COMPOSE_FILES) --env-file .env build
	
logs:
	sudo docker compose $(COMPOSE_FILES) logs --tail=1000 --follow

all: down kill build up logs 