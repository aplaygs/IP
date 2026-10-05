"""Представления приложения applications.

Отображает список заявок участников ярмарок и детальную информацию
по конкретной заявке со статусом бронирования.
"""

from django.http import HttpResponse

from homepage.views import page
from models.applications import find_application_by_id
from storage import load_applications, load_fairs, load_vendors


def applications(request) -> HttpResponse:
    """Отображает список всех заявок участников."""
    fairs_list = load_fairs("data/fairs.json")
    vendors_list = load_vendors("data/vendors.json")
    applications_list = load_applications(
        "data/applications.json",
        fairs_list,
        vendors_list,
    )

    items = ""
    for app in applications_list:
        status = "отменено" if app.is_cancelled else "активно"
        badge = "bg-secondary" if app.is_cancelled else "bg-success"
        items += f"""
    <li class="list-group-item d-flex justify-content-between
               align-items-center">
      <a href="/applications/{app.id}/">
        Заявка #{app.id}: {app.vendor.name} – {app.fair.name}
      </a>
      <span class="badge {badge}">{status}</span>
    </li>
    """

    content = f"""
  <h1>Заявки участников</h1>
  <p class="text-muted">Реестр поданных заявок на участие в ярмарках</p>
  <ul class="list-group">
    {items}
  </ul>
  """
    return HttpResponse(page("FairVendor – заявки", content))


def application_detail(request, application_id: int) -> HttpResponse:
    """Отображает детальную информацию по конкретной заявке."""
    fairs_list = load_fairs("data/fairs.json")
    vendors_list = load_vendors("data/vendors.json")
    applications_list = load_applications(
        "data/applications.json",
        fairs_list,
        vendors_list,
    )

    app = find_application_by_id(applications_list, application_id)
    if app is None:
        content = """
    <h1 class="text-danger">Заявка не найдена</h1>
    <a href="/applications/" class="btn btn-outline-secondary">
      ← к списку заявок
    </a>
    """
        return HttpResponse(
            page("Заявка не найдена", content),
            status=404,
        )

    status = "отменено" if app.is_cancelled else "активно"
    badge = "bg-secondary" if app.is_cancelled else "bg-success"
    content = f"""
  <div class="card">
    <div class="card-body">
      <h5 class="card-title">Заявка №{app.id}</h5>
      <p class="card-text">
        <strong>Ярмарка:</strong> {app.fair.name}
      </p>
      <p class="card-text">
        <strong>Продавец (бренд):</strong> {app.vendor.name}
      </p>
      <p class="card-text">
        <strong>ИНН продавца:</strong> {app.vendor.inn}
      </p>
      <p class="card-text">
        <strong>Категория товаров:</strong> {app.vendor.category}
      </p>
      <p class="card-text">
        <strong>Запрошенная площадь:</strong> {app.requested_space:.1f} кв.м
      </p>
      <p class="card-text">
        <strong>Сбор за участие:</strong> {app.fee:,.2f} руб.
      </p>
      <p class="card-text">
        Статус:
        <span class="badge {badge}">{status}</span>
      </p>
      <a href="/applications/" class="btn btn-outline-secondary">
        ← к списку заявок
      </a>
    </div>
  </div>
  """
    return HttpResponse(
        page(f"Заявка №{app.id}", content),
        status=200,
    )
