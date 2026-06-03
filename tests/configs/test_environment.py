import os
from unittest import mock

from app.config.environment import (
    environment,
    check_dev_environment,
    is_environment_remote,
    is_environment_local,
)


def test_enviroment() -> None:
    environments = ["LOCAL", "Local", "lOCal"]
    lower_case_env = "local"
    for env in environments:
        with mock.patch.dict(os.environ, {"ENVIRONMENT": env}):
            assert environment() == lower_case_env


def test_check_dev_environment() -> None:
    dev_envs = ["development", "Development", "DEVELOPMENT"]
    for env in dev_envs:
        with mock.patch.dict(os.environ, {"ENVIRONMENT": env}):
            assert check_dev_environment() is True

    not_dev_envs = ["LOCAL", "PRODUCTION", "STAGING"]
    for env in not_dev_envs:
        with mock.patch.dict(os.environ, {"ENVIRONMENT": env}):
            assert check_dev_environment() is False


def test_is_environment_remote() -> None:
    remote_envs = [
        "DEVELOPMENT",
        "dEvelopment",
        "STAGING",
        "staging",
        "sTAging",
        "PRODUCTION",
        "producTion",
    ]
    for env in remote_envs:
        with mock.patch.dict(os.environ, {"ENVIRONMENT": env}):
            assert is_environment_remote() is True

    not_remote_envs = ["local", "LOCAL", "local", "test", "TEST", "tEst"]
    for env in not_remote_envs:
        with mock.patch.dict(os.environ, {"ENVIRONMENT": env}):
            assert is_environment_remote() is False


def test_is_enviroment_local() -> None:
    local_envs = ["local", "LOCAL", "local", "test", "TEST"]
    for env in local_envs:
        with mock.patch.dict(os.environ, {"ENVIRONMENT": env}):
            assert is_environment_local() is True

    remote_envs = [
        "developement",
        "DEVELOPMENT",
        "STAGING",
        "staGing",
        "PRODUCTION",
        "production",
    ]
    for env in remote_envs:
        with mock.patch.dict(os.environ, {"ENVIRONMENT": env}):
            assert is_environment_local() is False
