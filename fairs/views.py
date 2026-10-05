"""Представления приложения fairs.

Отображает список ярмарок и детальную информацию о конкретной ярмарке,
включая статус доступности торговых мест.
"""

from django.http import HttpResponse

from homepage.views import page
from models.applications import get_occupied_space
from models.fairs import find_fair_by_id
from storage import load_applications, load_fairs, load_vendors


def fairs(request) -> HttpResponse:
    """Отображает список всех доступных ярмарочных площадок."""
    fairs_list = load_fairs("data/fairs.json")
    items = ""
    for fair in fairs_list:
        text = (
            f"{fair.name} ({fair.location}) – "
            f"площадь {fair.total_space:.1f} кв.м"
        )
        items += (
            f'<li class="list-group-item d-flex justify-content-between '
            f'align-items-center">'
            f'<a href="/fairs/{fair.id}/">{text}</a>'
            f'<span class="badge bg-primary rounded-pill">'
            f'{fair.base_rate:.0f} руб./м²</span>'
            f'</li>'
        )

    content = f"""
  <h1>Ярмарки</h1>
  <p class="text-muted">Перечень актуальных ярмарок и выставок</p>
  <ul class="list-group">{items}</ul>
  """
    return HttpResponse(page("FairVendor – ярмарки", content))


def fair_detail(request, fair_id: int) -> HttpResponse:
    """Отображает детальную карточку выбранной ярмарки."""
    fairs_list = load_fairs("data/fairs.json")
    fair = find_fair_by_id(fairs_list, fair_id)

    if fair is None:
        content = """
    <h1 class="text-danger">Ярмарка не найдена</h1>
    <a href="/fairs/" class="btn btn-outline-secondary">
      ← к списку ярмарок
    </a>
    """
        return HttpResponse(
            page("Ярмарка не найдена", content),
            status=404,
        )

    vendors_list = load_vendors("data/vendors.json")
    applications_list = load_applications(
        "data/applications.json",
        fairs_list,
        vendors_list,
    )

    occupied = get_occupied_space(applications_list, fair.id)
    free_space = fair.get_free_space(occupied)
    available = free_space > 0
    status = "доступны места" if available else "мест нет"
    badge = "bg-success" if available else "bg-danger"

    content = f"""
  <div class="card">
    <div class="card-body">
      <h5 class="card-title">{fair.name}</h5>
      <p class="card-text"><strong>ID:</strong> {fair.id}</p>
      <p class="card-text"><strong>Площадка:</strong> {fair.location}</p>
      <p class="card-text"><strong>Дата проведения:</strong> {fair.date}</p>
      <p class="card-text">
        <strong>Базовая ставка:</strong> {fair.base_rate:,.2f} руб./кв.м
      </p>
      <p class="card-text">
        <strong>Общая площадь:</strong> {fair.total_space:.1f} кв.м
      </p>
      <p class="card-text">
        <strong>Свободная площадь:</strong> {free_space:.1f} кв.м
      </p>
      <p class="card-text">
        Доступность торговых мест:
        <span class="badge {badge}">{status}</span>
      </p>
      <a href="/fairs/" class="btn btn-outline-secondary">
        ← к списку ярмарок
      </a>
    </div>
  </div>
  """
    return HttpResponse(
        page(fair.name, content),
        status=200,
    )
