FROM python:3.13.3-alpine3.21
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ADD . /app

WORKDIR /app
RUN uv sync --frozen

ENTRYPOINT ["uv", "run", "emogic"]
