"""Общая реализация учёта на балансе."""

from vyshkat.domain.interfaces import Inventoried


class BalanceItem(Inventoried):
    """Базовый класс для всего, что стоит на балансе (транспорт и вещи)."""

    KIND = "объект"

    def __init__(self, model: str) -> None:
        if not model.strip():
            raise ValueError("Модель не может быть пустой")
        self._model = model.strip()
        self._inventory_number: str | None = None

    @property
    def kind(self) -> str:
        return self.KIND

    @property
    def name(self) -> str:
        return f"{self.KIND} «{self._model}»"

    @property
    def inventory_number(self) -> str | None:
        return self._inventory_number

    def assign_inventory_number(self, number: str) -> None:
        if self._inventory_number is not None:
            raise ValueError(f"У объекта уже есть номер {self._inventory_number}")
        self._inventory_number = number


def check_energy(value: float) -> float:
    """Проверка суточного расхода энергии."""
    if value < 0:
        raise ValueError("Расход энергии не может быть отрицательным")
    return float(value)
