"""Корневая конфигурация маршрутов проекта fairvendor."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("fairs/", include("fairs.urls")),
    path("applications/", include("applications.urls")),
]

handler404 = "homepage.views.page_not_found"
