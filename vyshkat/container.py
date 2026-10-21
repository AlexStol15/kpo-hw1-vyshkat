"""Сборка зависимостей (composition root)."""

import punq

from vyshkat.console import ConsoleApp
from vyshkat.services.beginner_policy import IBeginnerPolicy, SimplicityBeginnerPolicy
from vyshkat.services.fleet import Fleet, InventoryNumberGenerator
from vyshkat.services.reception import ReceptionService
from vyshkat.services.reports import FleetReports
from vyshkat.services.service_center import IServiceCenter, ServiceCenter


def build_container() -> punq.Container:
    container = punq.Container()
    singleton = punq.Scope.singleton
    container.register(Fleet, scope=singleton)
    container.register(InventoryNumberGenerator, scope=singleton)
    container.register(IServiceCenter, ServiceCenter, scope=singleton)
    container.register(IBeginnerPolicy, SimplicityBeginnerPolicy, scope=singleton)
    container.register(ReceptionService, scope=singleton)
    container.register(FleetReports, scope=singleton)
    container.register(ConsoleApp)
    return container
