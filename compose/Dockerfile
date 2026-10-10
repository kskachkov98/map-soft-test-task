FROM python:3.12-slim-bookworm as python-build-stage

# Установка системных зависимостей для сборки бинарных пакетов (например, psycopg)
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


# Копируем только файлы зависимостей Poetry
COPY pyproject.toml poetry.lock ./

# Экспортируем зависимости в requirements.txt
# Затем собираем wheels-пакеты в локальную директорию
ENV POETRY_VERSION=2.2.1
RUN pip install --upgrade pip \
    && pip install --no-cache-dir "poetry==$POETRY_VERSION"

# В Poetry 2.x обязательно нужно явно ставить плагин экспорта требований
RUN poetry self add poetry-plugin-export && \
    poetry export --without-hashes --format=requirements.txt > requirements.txt

RUN pip wheel --wheel-dir=/usr/src/app/wheels -r requirements.txt

# 'run' stage
FROM python:3.12-slim-bookworm as python-run-stage

ARG APP_HOME=/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install --no-install-recommends -y \
    # python dependencies
    python3-pip \
    # psycopg2 dependencies \
    postgresql-client libpq-dev \
    # make
    make \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*


COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

RUN pip3 install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/


# Copy entrypoint
COPY ./compose/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# Copy application code
COPY src ${APP_HOME}

# Copy files to fill db
COPY seed_files /seed_files/

ENTRYPOINT ["/entrypoint" ]
