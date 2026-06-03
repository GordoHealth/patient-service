from app.config.app_settings import AppSettings
from app.config.constants import (
    DEVELOPMENT_ENVIRONMENT,
    DEVTOOLS_ENVIRONMENTS,
    KUBERNETES_ENVIRONMENTS,
    LOCAL_ENVIRONMENTS
)


def environment() -> str:
    env: str = AppSettings().ENVIRONMENT.lower()
    return env


def check_dev_environment() -> bool:
    is_dev_environment: bool = environment() == DEVELOPMENT_ENVIRONMENT
    return is_dev_environment


def is_environment_devtools() -> bool:
    return environment() in DEVTOOLS_ENVIRONMENTS


def is_environment_remote() -> bool:
    return environment() in KUBERNETES_ENVIRONMENTS


def is_environment_local() -> bool:
    return environment() in LOCAL_ENVIRONMENTS
