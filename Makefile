.PHONY: logs kill down build all up restart clean purge

COMPOSE_FILES = -f docker-compose.yaml
ENV_FILE = --env-file .env

# Основные команды
restart:
	docker compose $(COMPOSE_FILES) restart bot

kill:
	docker compose $(COMPOSE_FILES) kill

down:
	docker compose $(COMPOSE_FILES) down

up:
	docker compose $(COMPOSE_FILES) up -d

build:
	docker compose $(COMPOSE_FILES) $(ENV_FILE) build --no-cache

logs:
	docker compose $(COMPOSE_FILES) logs --tail=1000 --follow

# Комплексные команды
all: down build up logs

# Новые полезные команды
clean: down
	docker system prune -f
	docker volume prune -f

purge: clean
	docker images purge
	docker builder prune -f

# Проверка состояния
status:
	docker compose $(COMPOSE_FILES) ps

# Проверка подключения к БД
db-check:
	docker compose exec db psql -U $$(grep POSTGRES_USER .env | cut -d '=' -f2) -d $$(grep POSTGRES_DB .env | cut -d '=' -f2) -c "SELECT 1"