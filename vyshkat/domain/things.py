"""Вещи на балансе (не прокатываются, техосмотр не проходят)."""

from vyshkat.domain.base import BalanceItem, check_energy
from vyshkat.domain.interfaces import EnergyConsumer


class Thing(BalanceItem):
    KIND = "Вещь"


class Helmet(Thing):
    KIND = "Шлем"


class DockStation(Thing, EnergyConsumer):
    KIND = "Док-станция"

    def __init__(self, model: str, daily_energy_kwh: float) -> None:
        super().__init__(model)
        self._daily_energy_kwh = check_energy(daily_energy_kwh)

    @property
    def daily_energy_kwh(self) -> float:
        return self._daily_energy_kwh


class ChargingCabinet(Thing, EnergyConsumer):
    KIND = "Зарядный шкаф"

    def __init__(self, model: str, daily_energy_kwh: float) -> None:
        super().__init__(model)
        self._daily_energy_kwh = check_energy(daily_energy_kwh)

    @property
    def daily_energy_kwh(self) -> float:
        return self._daily_energy_kwh
