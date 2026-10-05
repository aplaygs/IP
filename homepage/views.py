"""Представления приложения homepage.

Содержит вспомогательную функцию page() для формирования общего HTML-каркаса
страниц с подключением Bootstrap 5.3, главную страницу index() и обработчик
ошибки 404 page_not_found().
"""

from django.http import HttpResponse


def page(title: str, content: str) -> str:
    """Формирует каркас HTML-документа с навигацией и Bootstrap 5.3."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
  <nav class="nav p-3 mb-4 bg-light border-bottom">
    <a class="nav-link fw-bold text-dark" href="/">FairVendor</a>
    <a class="nav-link" href="/">Главная</a>
    <a class="nav-link" href="/fairs/">Ярмарки</a>
    <a class="nav-link" href="/applications/">Заявки</a>
  </nav>
  <main class="container">{content}</main>
</body>
</html>"""


def index(request) -> HttpResponse:
    """Отображает главную страницу сервиса FairVendor."""
    content = """
  <h1 class="display-4">FairVendor</h1>
  <p class="lead">Сервис регистрации продавцов на ярмарку.</p>
  <p>Основные разделы:</p>
  <div class="mt-3">
    <a href="/fairs/" class="btn btn-primary me-2">Ярмарки</a>
    <a href="/applications/" class="btn btn-secondary">Заявки</a>
  </div>
  """
    return HttpResponse(page("FairVendor", content))


def page_not_found(request, exception) -> HttpResponse:
    """Обработчик ошибки 404 (страница не найдена)."""
    content = """
  <h1 class="text-danger">404 – страница не найдена</h1>
  <p>Проверьте адрес или вернитесь на главную.</p>
  <a href="/" class="btn btn-primary">На главную</a>
  """
    return HttpResponse(
        page("404 – страница не найдена", content),
        status=404,
    )
