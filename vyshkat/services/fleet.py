"""Хранилище парка и выдача инвентарных номеров."""

from vyshkat.domain.interfaces import Inventoried
from vyshkat.domain.things import Thing
from vyshkat.domain.vehicles import Vehicle


class Fleet:
    """Хранит всё, что стоит на балансе. Ничего не решает и не считает."""

    def __init__(self) -> None:
        self._items: list[Inventoried] = []

    def add(self, item: Inventoried) -> None:
        if item.inventory_number is None:
            raise ValueError("Нельзя поставить на баланс объект без инвентарного номера")
        self._items.append(item)

    def items(self) -> list[Inventoried]:
        return list(self._items)

    def vehicles(self) -> list[Vehicle]:
        return [i for i in self._items if isinstance(i, Vehicle)]

    def things(self) -> list[Thing]:
        return [i for i in self._items if isinstance(i, Thing)]


class InventoryNumberGenerator:
    """Последовательные номера вида VK-0001."""

    def __init__(self, prefix: str = "VK") -> None:
        self._prefix = prefix
        self._counter = 0

    def next_number(self) -> str:
        self._counter += 1
        return f"{self._prefix}-{self._counter:04d}"
