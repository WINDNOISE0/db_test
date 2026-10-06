FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:0.12.23 /uv /uvx /bin/

ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_LINK_MODE=copy \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    PATH="/opt/venv/bin:$PATH" \
    HEADLESS=true

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked
RUN playwright install --with-deps chromium

CMD ["pytest", "tests/ui/test_network_mocking.py"]