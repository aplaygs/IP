"""Маршруты приложения fairs."""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.fairs, name="fairs"),
    path("<int:fair_id>/", views.fair_detail, name="fair_detail"),
]
