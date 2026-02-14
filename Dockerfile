FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY . .
RUN uv sync --frozen --no-cache
RUN uv run embed.py
CMD ["/app/.venv/bin/uvicorn", "main:app", "--port", "5000", "--host", "0.0.0.0"]