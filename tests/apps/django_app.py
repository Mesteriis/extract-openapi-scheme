# flake8: noqa
# sourcery skip: dont-import-test-modules
import os
import sys
from pathlib import Path

from django.conf import settings
from django.core.wsgi import get_wsgi_application

# Определение настроек Django
BASE_DIR = os.path.dirname(str(Path(__file__).resolve().parent.absolute()))

settings.configure(
    DEBUG=True,
    SECRET_KEY='your-secret-key',
    ROOT_URLCONF=sys.modules[__name__],
    MIDDLEWARE=[
        'django.middleware.common.CommonMiddleware',
    ],
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'rest_framework',
        'drf_spectacular',
    ],
    REST_FRAMEWORK={
        'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    },
    STATIC_URL='/static/',
)

import django # noqa: E402
from django.urls import path, include  # noqa: E402
from rest_framework import serializers, viewsets, routers  # noqa: E402
from rest_framework.response import Response  # noqa: E402
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView  # noqa: E402

django.setup()


class Item:
    def __init__(self, id, name):
        self.id = id
        self.name = name


items = [
    Item(1, 'Item 1'),
    Item(2, 'Item 2'),
]


class ItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)


class ItemViewSet(viewsets.ViewSet):
    serializer_class = ItemSerializer

    def list(self, request): # noqa
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)


router = routers.DefaultRouter()
router.register(r'items', ItemViewSet, basename='item')

urlpatterns = [
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
]
application = get_wsgi_application()
