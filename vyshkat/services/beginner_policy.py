"""Правило «подходит ли транспорт новичку»."""

from abc import ABC, abstractmethod

from vyshkat.domain.vehicles import Vehicle


class IBeginnerPolicy(ABC):
    @abstractmethod
    def is_suitable(self, vehicle: Vehicle) -> bool:
        """Можно ли выдать транспорт новичку."""


class SimplicityBeginnerPolicy(IBeginnerPolicy):
    """простота >= порога (по умолчанию 6)."""

    def __init__(self, threshold: int = 6) -> None:
        self._threshold = threshold

    def is_suitable(self, vehicle: Vehicle) -> bool:
        return vehicle.simplicity >= self._threshold
