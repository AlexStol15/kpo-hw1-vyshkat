"""Прокатный транспорт."""

from vyshkat.domain.base import BalanceItem, check_energy
from vyshkat.domain.interfaces import EnergyConsumer


class Vehicle(BalanceItem):
    """Прокатный транспорт: имеет простоту для новичка и износ."""

    KIND = "Транспорт"

    def __init__(self, model: str, simplicity: int, wear_percent: int = 0) -> None:
        super().__init__(model)
        if not 1 <= simplicity <= 10:
            raise ValueError("Простота для новичка должна быть от 1 до 10")
        if not 0 <= wear_percent <= 100:
            raise ValueError("Износ должен быть от 0 до 100%")
        self._simplicity = simplicity
        self._wear_percent = wear_percent

    @property
    def simplicity(self) -> int:
        return self._simplicity

    @property
    def wear_percent(self) -> int:
        return self._wear_percent


class Bicycle(Vehicle):
    """Обычный велосипед — энергию не потребляет."""

    KIND = "Велосипед"


class ElectricScooter(Vehicle, EnergyConsumer):
    KIND = "Электросамокат"

    def __init__(self, model: str, simplicity: int, daily_energy_kwh: float,
                 wear_percent: int = 0) -> None:
        super().__init__(model, simplicity, wear_percent)
        self._daily_energy_kwh = check_energy(daily_energy_kwh)

    @property
    def daily_energy_kwh(self) -> float:
        return self._daily_energy_kwh


class ElectricBike(Vehicle, EnergyConsumer):
    KIND = "Электровелосипед"

    def __init__(self, model: str, simplicity: int, daily_energy_kwh: float,
                 wear_percent: int = 0) -> None:
        super().__init__(model, simplicity, wear_percent)
        self._daily_energy_kwh = check_energy(daily_energy_kwh)

    @property
    def daily_energy_kwh(self) -> float:
        return self._daily_energy_kwh
