# sourcery skip: dont-import-test-modules
import pytest


@pytest.fixture()
def extractor():
    from extractor import Extractor

    return Extractor


@pytest.fixture()
def fastapi_app_path():
    return "tests.apps.fastapi:app"


@pytest.fixture()
def fastapi_app():
    from tests.apps.fastapi import app

    return app


@pytest.fixture()
def django_app_path():
    return "tests.apps.django_app:application"


@pytest.fixture()
def django_app():
    from tests.apps.django_app import application

    return application
