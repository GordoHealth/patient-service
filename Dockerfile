# STAGE 1: Base
FROM python:3.13-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /usr/src

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libboost-all-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip pipenv
COPY ./Pipfile ./Pipfile.lock ./

# STAGE 2: Development & Testing (CI/CD / Local)
FROM base AS development

RUN pipenv sync --dev --system

COPY . /usr/src/

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

# STAGE 3: Production (Staging & Prod)
FROM base AS production

RUN pipenv sync --system --clear

COPY . /usr/src/

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser /usr/src

RUN chmod +x /usr/src/docker-entrypoint.sh
USER appuser
EXPOSE 8000

ENTRYPOINT ["/usr/src/docker-entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
