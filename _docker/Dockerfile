FROM python:3.12-slim

ENV USER=app-user \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/usr/local


RUN apt-get update && apt-get install --no-install-recommends -y \
    curl libpq-dev python3-dev build-essential\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -s /bin/bash $USER

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV APP_DIR=/home/$USER/src

RUN mkdir $APP_DIR
RUN mkdir $APP_DIR/staticfiles

WORKDIR $APP_DIR

RUN --mount=type=cache,target=/home/$USER/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project


COPY ../pyproject.toml uv.lock $APP_DIR
COPY ../src $APP_DIR

RUN --mount=type=cache,target=/home/$USER/.cache/uv \
    uv sync --frozen

ENV PYTHONPATH=$APP_DIR

RUN uv run python manage.py collectstatic --no-input

RUN chown -R "$USER":"$USER" $APP_DIR
USER $USER

EXPOSE 8000


# Start Gunicorn zonder venv
CMD ["gunicorn", "_project.wsgi:application", "--bind", "0.0.0.0:8000"]