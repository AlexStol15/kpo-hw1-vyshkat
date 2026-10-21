"""Приёмка техники и постановка вещей на баланс."""

from vyshkat.domain.things import Thing
from vyshkat.domain.vehicles import Vehicle
from vyshkat.services.fleet import Fleet, InventoryNumberGenerator
from vyshkat.services.service_center import InspectionResult, IServiceCenter


class ReceptionService:
    def __init__(self, fleet: Fleet, service_center: IServiceCenter,
                 numbers: InventoryNumberGenerator) -> None:
        self._fleet = fleet
        self._service_center = service_center
        self._numbers = numbers

    def receive_vehicle(self, vehicle: Vehicle) -> InspectionResult:
        """Транспорт попадает в парк только после успешного техосмотра."""
        result = self._service_center.inspect(vehicle)
        if result.accepted:
            vehicle.assign_inventory_number(self._numbers.next_number())
            self._fleet.add(vehicle)
        return result

    def register_thing(self, thing: Thing) -> str:
        """Вещи ставятся на баланс без техосмотра."""
        number = self._numbers.next_number()
        thing.assign_inventory_number(number)
        self._fleet.add(thing)
        return number
