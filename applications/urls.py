"""Маршруты приложения applications."""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.applications, name="applications"),
    path(
        "<int:application_id>/",
        views.application_detail,
        name="application_detail",
    ),
]
