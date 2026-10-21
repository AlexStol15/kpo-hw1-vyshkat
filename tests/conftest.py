import pytest

from vyshkat.container import build_container
from vyshkat.services.service_center import InspectionResult, IServiceCenter


class StubServiceCenter(IServiceCenter):
    """Заглушка техосмотра: всегда возвращает заранее заданное решение."""

    def __init__(self, accept: bool) -> None:
        self.accept = accept
        self.inspected = []

    def inspect(self, vehicle):
        self.inspected.append(vehicle)
        return InspectionResult(self.accept, "stub")


@pytest.fixture
def container():
    return build_container()


def container_with_service_center(service_center: IServiceCenter):
    """Тот же контейнер приложения, но техосмотр подменён через DI."""
    container = build_container()
    container.register(IServiceCenter, instance=service_center)
    return container
