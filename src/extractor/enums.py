from enum import Enum


class FrameworkTypeEnum(str, Enum):
    FASTAPI = "fastapi"
    DJANGO = "django"


class DjangoDocLibryaryEnum(str, Enum):
    DRF_SPECTACULAR = "drf_spectacular"
    DRF_YASG = "drf_yasg"
