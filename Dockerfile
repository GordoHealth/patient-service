ARG REGISTRY
FROM ${REGISTRY}/python:3.13-slim-bookworm

ARG ENVIRONMENT
ENV ENVIRONMENT=${ENVIRONMENT}

WORKDIR /usr/src

# Don't make any .pyc files on import.
# https://docs.python.org/3/using/cmdline.html#envvar-PYTHONDONTWRITEBYTECODE
ENV PYTHONDONTWRITEBYTECODE=1

# Enable quicker printing and logging.
# https://docs.python.org/3/using/cmdline.html#envvar-PYTHONUNBUFFERED
ENV PYTHONUNBUFFERED=1

# It's required to run these commands to make sure that contrast can be installed in Linux OS
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libboost-all-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip pipenv

COPY ./Pipfile ./Pipfile.lock ./

RUN pipenv sync --dev --system

COPY . /usr/src/

RUN cp docker-entrypoint.sh /usr/local/bin \
  && chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["docker-entrypoint.sh"]
