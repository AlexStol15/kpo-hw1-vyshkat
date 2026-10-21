import pytest

from tests.conftest import StubServiceCenter, container_with_service_center
from vyshkat.domain.things import DockStation, Helmet
from vyshkat.domain.vehicles import Bicycle, ElectricBike, ElectricScooter, Vehicle
from vyshkat.services.beginner_policy import IBeginnerPolicy, SimplicityBeginnerPolicy
from vyshkat.services.reception import ReceptionService
from vyshkat.services.reports import FleetReports


@pytest.fixture
def filled():
    c = container_with_service_center(StubServiceCenter(accept=True))
    reception = c.resolve(ReceptionService)
    reception.receive_vehicle(ElectricScooter("Easy", simplicity=6, daily_energy_kwh=0.5))
    reception.receive_vehicle(ElectricScooter("Hard", simplicity=5, daily_energy_kwh=0.7))
    reception.receive_vehicle(Bicycle("Bike", simplicity=9))
    reception.register_thing(Helmet("H"))
    reception.register_thing(DockStation("D", daily_energy_kwh=2.0))
    return c


def test_units_count(filled):
    reports = filled.resolve(FleetReports)
    assert reports.total_units() == 5
    assert reports.units_by_kind() == {
        "Электросамокат": 2, "Велосипед": 1, "Шлем": 1, "Док-станция": 1}


def test_total_energy_includes_vehicles_and_things(filled):
    assert filled.resolve(FleetReports).total_daily_energy_kwh() == pytest.approx(3.2)


def test_beginner_rule_threshold_is_six(filled):
    names = [v.name for v in filled.resolve(FleetReports).beginner_vehicles()]
    assert names == ["Электросамокат «Easy»", "Велосипед «Bike»"]  # 5 не прошёл, 6 прошёл


def test_beginner_policy_can_be_replaced_through_di(filled):
    class NoElectricForBeginners(IBeginnerPolicy):
        def is_suitable(self, vehicle: Vehicle) -> bool:
            return SimplicityBeginnerPolicy().is_suitable(vehicle) and isinstance(vehicle, Bicycle)

    filled.register(IBeginnerPolicy, instance=NoElectricForBeginners())
    filled.register(FleetReports)  # пересобрать отчёты с новой политикой
    names = [v.name for v in filled.resolve(FleetReports).beginner_vehicles()]
    assert names == ["Велосипед «Bike»"]


def test_inventory_list_has_vehicles_and_things(filled):
    rows = filled.resolve(FleetReports).inventory_list()
    assert [n for n, _ in rows] == ["VK-0001", "VK-0002", "VK-0003", "VK-0004", "VK-0005"]
    assert ("VK-0004", "Шлем «H»") in rows


def test_empty_fleet_reports(container):
    reports = container.resolve(FleetReports)
    assert reports.total_units() == 0
    assert reports.total_daily_energy_kwh() == 0
    assert reports.beginner_vehicles() == []


def test_electric_bike_counts_energy():
    c = container_with_service_center(StubServiceCenter(accept=True))
    c.resolve(ReceptionService).receive_vehicle(ElectricBike("E", 6, 1.5))
    assert c.resolve(FleetReports).total_daily_energy_kwh() == pytest.approx(1.5)
