# LLM Bot

# Development

## Подготовка к разработке

Чтобы начать работу с проектом, необходимо выполнить следующие шаги:

1. Установить Docker и Docker Compose
2. Скопировать конфиги
 - config.toml
 - postgrest.env
 - .env
3. Запустить infra контейнеры: `docker compose --profile infra up -d`
4. Инициализировать pre-commit hooks: `uv run pre-commit install`
