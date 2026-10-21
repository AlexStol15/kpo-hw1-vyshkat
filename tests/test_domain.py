import pytest

from vyshkat.domain.interfaces import EnergyConsumer, Inventoried
from vyshkat.domain.things import ChargingCabinet, DockStation, Helmet
from vyshkat.domain.vehicles import Bicycle, ElectricBike, ElectricScooter


@pytest.mark.parametrize("simplicity", [0, 11])
def test_simplicity_out_of_range_is_rejected(simplicity):
    with pytest.raises(ValueError):
        Bicycle("B", simplicity=simplicity)


def test_wear_out_of_range_is_rejected():
    with pytest.raises(ValueError):
        Bicycle("B", simplicity=5, wear_percent=150)


def test_negative_energy_is_rejected():
    with pytest.raises(ValueError):
        ElectricScooter("S", simplicity=5, daily_energy_kwh=-1)
    with pytest.raises(ValueError):
        DockStation("D", daily_energy_kwh=-0.1)


def test_empty_model_is_rejected():
    with pytest.raises(ValueError):
        Helmet("   ")


def test_inventory_number_can_be_assigned_only_once():
    helmet = Helmet("H")
    assert helmet.inventory_number is None
    helmet.assign_inventory_number("VK-0001")
    assert helmet.inventory_number == "VK-0001"
    with pytest.raises(ValueError):
        helmet.assign_inventory_number("VK-0002")


def test_energy_consumers_are_marked_by_interface():
    assert isinstance(ElectricScooter("S", 5, 0.5), EnergyConsumer)
    assert isinstance(ElectricBike("E", 5, 1.0), EnergyConsumer)
    assert isinstance(ChargingCabinet("C", 3.0), EnergyConsumer)
    assert not isinstance(Bicycle("B", 5), EnergyConsumer)
    assert not isinstance(Helmet("H"), EnergyConsumer)


def test_everything_on_balance_is_inventoried():
    for item in (Bicycle("B", 5), Helmet("H"), DockStation("D", 1.0)):
        assert isinstance(item, Inventoried)


def test_name_contains_kind_and_model():
    assert ElectricScooter("Ninebot", 7, 0.5).name == "Электросамокат «Ninebot»"
