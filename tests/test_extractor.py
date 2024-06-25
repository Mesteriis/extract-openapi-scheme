import random

from extractor.enums import FrameworkTypeEnum


def test_find_app_fastapi(extractor, fastapi_app_path):
    ext = extractor(fastapi_app_path)
    app = ext._app
    assert app is not None, "Application not found."

    from fastapi import FastAPI
    assert isinstance(app, FastAPI), "Application is not a FastAPI."


def test_find_app_django(extractor, django_app_path):
    ext = extractor(django_app_path)
    app = ext._app
    assert app is not None, "Application not found."

    from django.core.handlers.wsgi import WSGIHandler
    assert isinstance(app, WSGIHandler), "Application is not a django.WSGIHandler."


def test_detect_framework(extractor, fastapi_app_path, django_app_path):
    path, framework = random.choice(
        [
            (fastapi_app_path, FrameworkTypeEnum.FASTAPI),
            (django_app_path, FrameworkTypeEnum.DJANGO)
        ],
    )
    ext = extractor(path)
    ext._detect_framework()
    assert ext._framework == framework, "Framework not detected correctly."


def test_extract_scheme(extractor, fastapi_app_path, django_app_path):
    app = random.choice([fastapi_app_path, django_app_path])
    ext = extractor(app)
    openapi_data = ext.extract_scheme()
    assert openapi_data, "OpenAPI data not extracted."
    assert isinstance(openapi_data, dict), "OpenAPI data is not a dictionary."
    assert "openapi" in openapi_data, "OpenAPI version not found."

