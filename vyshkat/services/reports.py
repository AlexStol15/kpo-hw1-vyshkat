"""Отчёты по парку."""

from collections import Counter

from vyshkat.domain.interfaces import EnergyConsumer
from vyshkat.domain.vehicles import Vehicle
from vyshkat.services.beginner_policy import IBeginnerPolicy
from vyshkat.services.fleet import Fleet


class FleetReports:
    def __init__(self, fleet: Fleet, beginner_policy: IBeginnerPolicy) -> None:
        self._fleet = fleet
        self._policy = beginner_policy

    def total_units(self) -> int:
        return len(self._fleet.items())

    def units_by_kind(self) -> dict[str, int]:
        return dict(Counter(item.kind for item in self._fleet.items()))

    def total_daily_energy_kwh(self) -> float:
        return sum(i.daily_energy_kwh for i in self._fleet.items()
                   if isinstance(i, EnergyConsumer))

    def beginner_vehicles(self) -> list[Vehicle]:
        return [v for v in self._fleet.vehicles() if self._policy.is_suitable(v)]

    def inventory_list(self) -> list[tuple[str, str]]:
        """Пары (инвентарный номер, наименование) для техники и вещей."""
        return sorted((i.inventory_number, i.name) for i in self._fleet.items())
