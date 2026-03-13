FROM python:3.12-slim AS builder

WORKDIR /app

RUN pip install --no-cache-dir "uv~=0.10.4"

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY src/ ./src/
COPY alembic.ini ./

ENV PYTHONPATH=/app

FROM builder AS dev

CMD ["uvicorn", "src.bot.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000", "--factory"]

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /app /app
COPY alembic.ini ./

ENV PYTHONPATH=/app
ENV PATH="/app/.venv/bin:$PATH"
# mrmamongo: Needed for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

CMD ["uvicorn", "src.bot.main:app", "--host", "0.0.0.0", "--port", "8000", "--factory"]
