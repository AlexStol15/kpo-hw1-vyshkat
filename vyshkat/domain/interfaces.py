"""Базовые абстракции предметной области."""

from abc import ABC, abstractmethod


class Inventoried(ABC):
    """Объект, который ставится на баланс и имеет инвентарный номер."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Человекочитаемое наименование."""

    @property
    @abstractmethod
    def inventory_number(self) -> str | None:
        """Инвентарный номер (None, пока объект не поставлен на баланс)."""

    @abstractmethod
    def assign_inventory_number(self, number: str) -> None:
        """Присвоить инвентарный номер (один раз)."""


class EnergyConsumer(ABC):
    """Устройство, потребляющее электроэнергию."""

    @property
    @abstractmethod
    def daily_energy_kwh(self) -> float:
        """Суточный расход энергии, кВт·ч."""
