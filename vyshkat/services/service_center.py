"""Техосмотр: решает, принимать ли транспорт в парк."""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from vyshkat.domain.interfaces import EnergyConsumer
from vyshkat.domain.vehicles import Vehicle


@dataclass(frozen=True)
class InspectionResult:
    accepted: bool
    reason: str


class IServiceCenter(ABC):
    @abstractmethod
    def inspect(self, vehicle: Vehicle) -> InspectionResult:
        """Провести техосмотр."""


class ServiceCenter(IServiceCenter):
    """Реальный техосмотр: ограничение по износу и по расходу энергии."""

    def __init__(self, max_wear_percent: int = 30, max_daily_energy_kwh: float = 3.0) -> None:
        self._max_wear = max_wear_percent
        self._max_energy = max_daily_energy_kwh

    def inspect(self, vehicle: Vehicle) -> InspectionResult:
        if vehicle.wear_percent > self._max_wear:
            return InspectionResult(
                False, f"износ {vehicle.wear_percent}% больше допустимых {self._max_wear}%")
        if isinstance(vehicle, EnergyConsumer) and vehicle.daily_energy_kwh > self._max_energy:
            return InspectionResult(
                False, f"расход {vehicle.daily_energy_kwh} кВт·ч больше допустимых "
                       f"{self._max_energy} кВт·ч")
        return InspectionResult(True, "техосмотр пройден")
