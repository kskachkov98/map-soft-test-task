# Переменные для локального запуска
PYTHON = poetry run python
UVICORN = poetry run uvicorn
SRC_DIR = src

# Имя основного веб-сервиса в вашем docker-compose.yml
DOCKER_SERVICE_BACKEND = backend

.PHONY: help build run run-local db-init db-init-local db-seed db-seed-local setup setup-local

help:
	@echo "Доступные Docker-команды:"
	@echo "  make build          - Собрать/пересобрать Docker-образы"
	@echo "  make run            - Запустить всю инфраструктуру в Docker (FastAPI + Postgres)"
	@echo "  make db-init        - Создать схему таблиц внутри запущенного Docker-контейнера"
	@echo "  make db-seed        - Залить JSON-данные внутрь запущенного Docker-контейнера"
	@echo "  make setup          - Полный цикл в Docker: билд, запуск и подготовка базы"
	@echo ""
	@echo "Доступные Local-команды (без Docker):"
	@echo "  make run-local      - Запустить FastAPI приложение локально на хосте"
	@echo "  make db-init-local  - Создать схему таблиц в локальной PostgreSQL"
	@echo "  make db-seed-local  - Наполнить локальную базу данных из JSON-файла"
	@echo "  make setup-local    - Полный цикл локально: создание таблиц, сид и запуск"

# ==============================================================================
# КОМАНДЫ ДЛЯ СРЕДЫ DOCKER
# ==============================================================================

# Билд контейнеров
build:
	@echo "==> Сборка образов Docker Compose..."
	docker compose build

# Запуск инфраструктуры в фоне (или логами в терминал)
run:
	@echo "==> Запуск контейнеров (FastAPI + PostgreSQL)..."
	docker compose up

# Создание схемы внутри Docker
db-init:
	@echo "==> [Docker] Создание таблиц..."
	docker compose up -d
	docker compose exec $(DOCKER_SERVICE_BACKEND) python -m scripts.init_db

# Сидинг данных внутри Docker
db-seed:
	@echo "==> [Docker] Наполнение базы данных..."
	docker compose up -d
	docker compose exec $(DOCKER_SERVICE_BACKEND) python -m scripts.seed_db

# Полный цикл разворачивания в Docker одной командой
setup:
	@echo "==> Полный запуск инфраструктуры в Docker..."
	docker compose up -d --build
	@echo "Ожидание инициализации СУБД..."
	sleep 3
	make db-init
	make db-seed
	@echo "🎉 Все сервисы настроены и работают в фоне! Логи: docker compose logs -f"

# ==============================================================================
# КОМАНДЫ ДЛЯ ЛОКАЛЬНОЙ СРЕДЫ (LOCAL / HOST)
# ==============================================================================

# Запуск приложения локально
run-local:
	@echo "==> [Local] Запуск FastAPI с переменными из .env..."
	env $$(cat .envs/.env | xargs) PYTHONPATH=$(SRC_DIR) $(UVICORN) src.main:app --reload --host 0.0.0.0 --port 8000
