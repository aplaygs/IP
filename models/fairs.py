"""Модуль модели ярмарки (Fair).

Определяет класс Fair для представления ярмарочного мероприятия, его атрибутов,
расчета доступных площадей, строкового представления и сериализации.
"""

from typing import Any, Dict, List, Optional


class Fair:
    """Класс, представляющий ярмарочное мероприятие."""

    def __init__(
        self,
        fair_id: int,
        name: str,
        location: str,
        date: str,
        base_rate: float,
        total_space: float,
    ) -> None:
        """Инициализирует объект ярмарки с валидацией базовых параметров."""
        if fair_id <= 0:
            raise ValueError(
                "Идентификатор ярмарки должен быть положительным."
            )
        clean_name = name.strip()
        if not clean_name:
            raise ValueError("Название ярмарки не может быть пустым.")
        if base_rate <= 0:
            raise ValueError(
                "Базовая арендная ставка должна быть больше нуля."
            )
        if total_space <= 0:
            raise ValueError("Общая площадь ярмарки должна быть больше нуля.")

        self.id = fair_id
        self.name = clean_name
        self.location = location.strip()
        self.date = date.strip()
        self.base_rate = float(base_rate)
        self.total_space = float(total_space)

    def is_space_available(
        self, requested_space: float, occupied_space: float
    ) -> bool:
        """Проверяет возможность размещения стенда запрашиваемой площади."""
        if requested_space <= 0:
            return False
        return (occupied_space + requested_space) <= self.total_space

    def get_free_space(self, occupied_space: float) -> float:
        """Возвращает размер свободной торговой площади на площадке."""
        return max(0.0, round(self.total_space - occupied_space, 2))

    def __getitem__(self, item: str) -> Any:
        """Поддержка доступа по ключу для обратной совместимости."""
        if hasattr(self, item):
            return getattr(self, item)
        raise KeyError(item)

    def __contains__(self, item: str) -> bool:
        """Проверка наличия атрибута как ключа словаря."""
        return hasattr(self, item)

    def __str__(self) -> str:
        """Возвращает строковое представление ярмарки."""
        return (
            f"Ярмарка #{self.id} «{self.name}» ({self.location}, "
            f"дата: {self.date}, ставка: {self.base_rate:.2f} руб./кв.м, "
            f"площадь: {self.total_space:.1f} кв.м)"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Преобразует объект ярмарки в словарь для сохранения в JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "base_rate": self.base_rate,
            "total_space": self.total_space,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Fair":
        """Создает экземпляр класса Fair из словаря данных."""
        return cls(
            fair_id=data["id"],
            name=data["name"],
            location=data.get("location", ""),
            date=data.get("date", ""),
            base_rate=float(data["base_rate"]),
            total_space=float(data["total_space"]),
        )


def find_fair_by_id(fairs: List[Fair], fair_id: int) -> Optional[Fair]:
    """Находит ярмарку по уникальному идентификатору."""
    for fair in fairs:
        if fair.id == fair_id:
            return fair
    return None
