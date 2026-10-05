"""Автоматические тесты для представлений (views) веб-приложения FairVendor.

Проверяет корректность формирования HTTP-ответов, маршрутизации URL,
кодов статусов (200 и 404), а также наличие ключевых элементов разметки.
"""

import os
import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fairvendor.settings")
django.setup()

from django.conf import settings  # noqa: E402
from django.test import Client  # noqa: E402
from models.applications import find_application_by_id  # noqa: E402
from models.fairs import find_fair_by_id  # noqa: E402
from storage import load_applications, load_fairs  # noqa: E402


@pytest.fixture
def client():
    """Фикстура тестового HTTP-клиента Django."""
    return Client()


def test_homepage_index(client):
    """Проверка главной страницы: код 200 и ссылки на разделы."""
    response = client.get("/")
    assert response.status_code == 200
    html = response.content.decode("utf-8")
    assert "FairVendor" in html
    assert 'href="/fairs/"' in html
    assert 'href="/applications/"' in html


def test_fairs_list(client):
    """Проверка списка ярмарок: код 200 и список площадок."""
    response = client.get("/fairs/")
    assert response.status_code == 200
    html = response.content.decode("utf-8")
    assert "Ярмарки" in html
    assert "list-group" in html


def test_fair_detail_success(client):
    """Проверка детальной страницы существующей ярмарки: код 200."""
    fairs = load_fairs()
    assert len(fairs) > 0, "Необходима хотя бы одна ярмарка в data/fairs.json"
    target_fair = fairs[0]

    response = client.get(f"/fairs/{target_fair.id}/")
    assert response.status_code == 200
    html = response.content.decode("utf-8")
    assert target_fair.name in html
    assert "card" in html
    assert "Доступность торговых мест" in html
    assert 'href="/fairs/"' in html


def test_fair_detail_not_found(client):
    """Проверка запроса несуществующей ярмарки: код 404."""
    response = client.get("/fairs/999999/")
    assert response.status_code == 404
    html = response.content.decode("utf-8")
    assert "Ярмарка не найдена" in html
    assert 'href="/fairs/"' in html


def test_applications_list(client):
    """Проверка списка заявок: код 200 и вывод реестра."""
    response = client.get("/applications/")
    assert response.status_code == 200
    html = response.content.decode("utf-8")
    assert "Заявки участников" in html
    assert "list-group" in html


def test_application_detail_success(client):
    """Проверка детальной страницы существующей заявки: код 200."""
    apps = load_applications()
    assert len(apps) > 0, "Необходима хотя бы одна заявка в данных"
    target_app = apps[0]

    response = client.get(f"/applications/{target_app.id}/")
    assert response.status_code == 200
    html = response.content.decode("utf-8")
    assert f"Заявка №{target_app.id}" in html
    assert target_app.fair.name in html
    assert target_app.vendor.name in html
    assert 'href="/applications/"' in html


def test_application_detail_not_found(client):
    """Проверка запроса несуществующей заявки: код 404."""
    response = client.get("/applications/999999/")
    assert response.status_code == 404
    html = response.content.decode("utf-8")
    assert "Заявка не найдена" in html
    assert 'href="/applications/"' in html


def test_custom_404_handler(client):
    """Проверка собственного обработчика 404 при DEBUG=False."""
    orig_debug = settings.DEBUG
    try:
        settings.DEBUG = False
        response = client.get("/nonexistent-page-url/")
        assert response.status_code == 404
        html = response.content.decode("utf-8")
        assert "404 – страница не найдена" in html
        assert 'href="/"' in html
    finally:
        settings.DEBUG = orig_debug


def test_find_helpers():
    """Проверка вспомогательных функций поиска по ID."""
    fairs = load_fairs()
    if fairs:
        first = fairs[0]
        assert find_fair_by_id(fairs, first.id) == first
        assert find_fair_by_id(fairs, -1) is None

    apps = load_applications()
    if apps:
        first_app = apps[0]
        assert find_application_by_id(apps, first_app.id) == first_app
        assert find_application_by_id(apps, -1) is None
