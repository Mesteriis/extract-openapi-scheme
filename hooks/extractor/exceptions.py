class BaseExtractorError(Exception):
    pass


class UnsupportedFrameworkError(BaseExtractorError):
    pass


class UnsupportedFileFormatError(BaseExtractorError):
    pass


class UnsupportedDocLibraryError(BaseExtractorError):
    pass
