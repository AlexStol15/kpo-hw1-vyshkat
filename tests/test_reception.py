from unittest.mock import Mock

import pytest

from tests.conftest import StubServiceCenter, container_with_service_center
from vyshkat.domain.things import Helmet
from vyshkat.domain.vehicles import Bicycle, ElectricScooter
from vyshkat.services.fleet import Fleet
from vyshkat.services.reception import ReceptionService
from vyshkat.services.service_center import InspectionResult, IServiceCenter


def test_accepted_vehicle_gets_number_and_goes_to_fleet():
    c = container_with_service_center(StubServiceCenter(accept=True))
    reception, fleet = c.resolve(ReceptionService), c.resolve(Fleet)
    scooter = ElectricScooter("S", 7, 0.5)

    result = reception.receive_vehicle(scooter)

    assert result.accepted
    assert scooter.inventory_number == "VK-0001"
    assert fleet.vehicles() == [scooter]


def test_rejected_vehicle_does_not_get_into_fleet():
    stub = StubServiceCenter(accept=False)
    c = container_with_service_center(stub)
    reception, fleet = c.resolve(ReceptionService), c.resolve(Fleet)
    bike = Bicycle("B", 9)

    result = reception.receive_vehicle(bike)

    assert not result.accepted
    assert bike.inventory_number is None
    assert fleet.items() == []
    assert stub.inspected == [bike]  # техосмотр действительно вызывался


def test_reception_always_asks_service_center_mock():
    mock = Mock(spec=IServiceCenter)
    mock.inspect.return_value = InspectionResult(False, "нет тормозов")
    c = container_with_service_center(mock)
    bike = Bicycle("B", 9)

    result = c.resolve(ReceptionService).receive_vehicle(bike)

    mock.inspect.assert_called_once_with(bike)
    assert result.reason == "нет тормозов"


def test_things_are_registered_without_inspection():
    stub = StubServiceCenter(accept=False)
    c = container_with_service_center(stub)
    helmet = Helmet("H")

    number = c.resolve(ReceptionService).register_thing(helmet)

    assert number == helmet.inventory_number
    assert c.resolve(Fleet).things() == [helmet]
    assert stub.inspected == []


def test_numbers_are_unique_across_vehicles_and_things():
    c = container_with_service_center(StubServiceCenter(accept=True))
    reception = c.resolve(ReceptionService)
    reception.receive_vehicle(Bicycle("B", 5))
    reception.register_thing(Helmet("H"))
    numbers = [i.inventory_number for i in c.resolve(Fleet).items()]
    assert numbers == ["VK-0001", "VK-0002"]


def test_fleet_refuses_item_without_number():
    with pytest.raises(ValueError):
        Fleet().add(Helmet("H"))
