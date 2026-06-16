##########################################################
##################  DOCKER ACTIONS ####################
##########################################################

up: down
	@echo ---- BUILD ---
	@docker-compose --profile local build
	@echo ----- UP -----
	@docker-compose --profile local up -d

test-up: down
	@docker-compose --profile test up -d
	# brings down the main instance of db and brings up the test db

log-backend:
	@docker logs -f ${APPLICATION_NAME}

log-database:
	@docker logs -f ${APPLICATION_NAME}-database

log-tail-backend:
	@docker logs -f -n 100 ${APPLICATION_NAME}

log-tail-database:
	@docker logs -f -n 100 ${APPLICATION_NAME}-database

down:
	@echo ---- DOWN ----
	@docker-compose --profile local --profile test down

##########################################################
######################  DB ACTIONS #######################
##########################################################

psql:
	@docker exec -it ${APPLICATION_NAME}-database psql -U ${DATABASE_USER} ${DATABASE_NAME}

psql-test:
	@docker exec -it ${APPLICATION_NAME}-database-test psql -U ${TEST_DATABASE_USER} ${TEST_DATABASE_NAME}

db db-setup:
	@make up
	@make migrate

drop-reset-db:
	@docker-compose --profile local --profile test down --volumes
	@make db-setup


##########################################################
##################  INSTALLATION       ###################
##########################################################
install:
	@pipenv sync --dev
	@pipenv clean

install-docker:
	@docker exec ${APPLICATION_NAME} pipenv lock
	
##########################################################
##################  MIGRATION ACTIONS  ###################
##########################################################
migrate:
	@docker exec ${APPLICATION_NAME} pipenv run alembic upgrade head

upgrade:
	@docker exec ${APPLICATION_NAME} pipenv run alembic upgrade +"$(count)"
# usage: make upgrade count=5


downgrade:
	@docker exec ${APPLICATION_NAME} pipenv run alembic downgrade -"$(count)"
# usage: make downgrade count=5


generate-migration:
	@docker exec ${APPLICATION_NAME} pipenv run alembic revision --autogenerate -m "$(message)"
# usage: make generate-migration message="add consumer table"

##########################################################
######################  TEST ACTIONS  ####################
##########################################################

t test: test-up
	@docker exec ${APPLICATION_NAME} pipenv run pytest "${file}"

test-failed: test-up
	@docker exec ${APPLICATION_NAME} pipenv run pytest --lf
# Used to run only the tests the failed the previous run

tu test-unit:
	@docker exec ${APPLICATION_NAME} pipenv run pytest -k "not feature"

tf test-feature: test-up
	@docker exec ${APPLICATION_NAME} pipenv run pytest -k "feature" -s
# Feature tests require a test DB. Make sure to run make test-up before running feature tests.

tc test-current: test-up
	@docker exec ${APPLICATION_NAME} pipenv run pytest -k "current" -s

coverage: test-up
	@docker exec ${APPLICATION_NAME} pipenv run pytest --cov --cov-report term-missing

coverage-html: test-up
	@docker exec ${APPLICATION_NAME} pipenv run pytest --cov --cov-report=html


##########################################################
##################  SECURITY & LINTING ###################
##########################################################

pip-audit:
	@docker exec ${APPLICATION_NAME} pipenv run pip-audit

sbom:
	@docker exec ${APPLICATION_NAME} pipenv run pip-audit --format cyclonedx-json -o sbom.json

secrets-create-baseline:
	@docker exec ${APPLICATION_NAME} pipenv run detect-secrets scan > .secrets.baseline

secrets-update-baseline:
	@docker exec ${APPLICATION_NAME} pipenv run detect-secrets scan --update .secrets.baseline

secrets-scan:
	@docker exec ${APPLICATION_NAME} pipenv run detect-secrets scan --baseline .secrets.baseline

mypy:
	@docker exec ${APPLICATION_NAME} pipenv run mypy .

bandit:
	@docker exec ${APPLICATION_NAME} pipenv run bandit -r .

black:
	@docker exec ${APPLICATION_NAME} pipenv run black .

safety:
	@docker exec ${APPLICATION_NAME} pipenv run safety check

licenses:
	@docker exec ${APPLICATION_NAME} pipenv run pip-licenses

lint:
	@docker exec ${APPLICATION_NAME} pipenv run flake8

check-sec: pip-audit mypy bandit safety lint