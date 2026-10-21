from vyshkat.domain.vehicles import Bicycle, ElectricBike, ElectricScooter
from vyshkat.services.service_center import ServiceCenter


def test_good_vehicle_passes_inspection():
    result = ServiceCenter().inspect(ElectricScooter("S", 7, 0.6, wear_percent=10))
    assert result.accepted


def test_worn_vehicle_is_rejected():
    result = ServiceCenter(max_wear_percent=30).inspect(Bicycle("B", 7, wear_percent=31))
    assert not result.accepted
    assert "износ" in result.reason


def test_wear_on_the_limit_is_accepted():
    assert ServiceCenter(max_wear_percent=30).inspect(Bicycle("B", 7, wear_percent=30)).accepted


def test_too_hungry_vehicle_is_rejected():
    result = ServiceCenter(max_daily_energy_kwh=3.0).inspect(ElectricBike("E", 5, 3.5))
    assert not result.accepted
    assert "расход" in result.reason


def test_bicycle_has_no_energy_limit():
    assert ServiceCenter(max_daily_energy_kwh=0.0).inspect(Bicycle("B", 5)).accepted
