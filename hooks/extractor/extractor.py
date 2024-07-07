from pathlib import Path
from typing import Any

from django.core.handlers.wsgi import WSGIHandler
from fastapi import FastAPI
from uvicorn.importer import import_from_string

from .enums import DjangoDocLibryaryEnum, FrameworkTypeEnum
from .exceptions import UnsupportedDocLibraryError, UnsupportedFileFormatError, UnsupportedFrameworkError


class Extractor:
    """
    The Extractor class is responsible for extracting the scheme from a given framework and saving it to a file.

    Attributes:
        _framework (FrameworkTypeEnum): The type of the framework.
        __app (FastAPI | WSGIHandler): The application instance.
        _uvicorn_path (str): The path to the uvicorn server.
        _django_doc_library (DjangoDocLibryaryEnum): The Django documentation library.
        _file (Path): The output file path.
    """

    _framework: FrameworkTypeEnum
    __app: FastAPI | WSGIHandler = None
    _uvicorn_path: str
    _django_doc_library: DjangoDocLibryaryEnum
    _file: Path

    def __init__(
        self,
        uvicorn_path: str,
        *,
        django_doc_library: DjangoDocLibryaryEnum = DjangoDocLibryaryEnum.DRF_SPECTACULAR,
        out_file_name: str | Path = "openapi.json",
    ):
        """
        The constructor for the Extractor class.

        Parameters:
            uvicorn_path (str): The path to the uvicorn server.
            django_doc_library (DjangoDocLibryaryEnum, optional): The Django documentation library. Defaults to DRF_SPECTACULAR.
            out_file_name (str | Path, optional): The output file name. Defaults to "openapi.json".
        """
        self._uvicorn_path = uvicorn_path
        self._django_doc_library = django_doc_library
        self._file = out_file_name if isinstance(out_file_name, Path) else Path(out_file_name)
        self._detect_framework()

    def extract_scheme(self) -> dict[str, Any]:
        """
        Extracts the scheme from the given framework.

        Returns:
            dict[str, Any]: The extracted scheme.

        Raises:
            NotImplementedError: If DRF_YASG is selected as the Django documentation library.
            UnsupportedDocLibraryError: If an unsupported documentation library is selected.
            UnsupportedFrameworkError: If an unsupported framework is selected.
        """
        if self._framework == FrameworkTypeEnum.FASTAPI:
            openapi = self._app.openapi()
        elif self._framework == FrameworkTypeEnum.DJANGO:
            if self._django_doc_library == DjangoDocLibryaryEnum.DRF_YASG:
                msg = "DRF_YASG is not supported yet."
                raise NotImplementedError(msg)
            elif self._django_doc_library == DjangoDocLibryaryEnum.DRF_SPECTACULAR:
                from drf_spectacular.generators import SchemaGenerator

                generator = SchemaGenerator()
                openapi = generator.get_schema(request=None, public=True)
            else:
                msg = f"Unsupported doc library: {self._django_doc_library}"
                raise UnsupportedDocLibraryError(msg)
        else:
            msg = f"Unsupported framework: {self._framework}"
            raise UnsupportedFrameworkError(msg)
        return openapi

    def save(self, openapi: dict):
        """
        Saves the extracted scheme to a file.

        Parameters:
            openapi (dict): The extracted scheme.

        Raises:
            UnsupportedFileFormatError: If an unsupported file format is selected.
        """
        if self._file.suffix == ".json":
            import json

            with self._file.open("w") as f:
                json.dump(openapi, f, indent=2)
        elif self._file.suffix == ".yaml":
            import yaml

            with self._file.open("w") as f:
                yaml.dump(openapi, f, sort_keys=False)
        else:
            msg = f"Unsupported format: {self._file.suffix}"
            raise UnsupportedFileFormatError(msg)

    def _detect_framework(self):
        """
        Detects the framework from the given application instance.

        Raises:
            UnsupportedFrameworkError: If an unsupported framework is detected.
        """
        if isinstance(self._app, FastAPI):
            self._framework = FrameworkTypeEnum.FASTAPI
        elif isinstance(self._app, WSGIHandler):
            self._framework = FrameworkTypeEnum.DJANGO
        else:
            msg = f"Unsupported framework: {self._uvicorn_path}"
            raise UnsupportedFrameworkError(msg)

    @property
    def _app(self):
        """
        Gets the application instance.

        Returns:
            FastAPI | WSGIHandler: The application instance.
        """
        if self.__app is None:
            self.__app = import_from_string(self._uvicorn_path)
        return self.__app
