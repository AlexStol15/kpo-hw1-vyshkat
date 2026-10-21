"""Консольный интерфейс. Только ввод/вывод — бизнес-логика в сервисах."""

from collections.abc import Callable

from vyshkat.domain.things import ChargingCabinet, DockStation, Helmet
from vyshkat.domain.vehicles import Bicycle, ElectricBike, ElectricScooter
from vyshkat.services.reception import ReceptionService
from vyshkat.services.reports import FleetReports

# Каталоги видов: новый вид = новый класс + одна строка здесь.
# (название, класс, нужен ли ввод расхода энергии)
VEHICLE_TYPES = {
    "1": ("Электросамокат", ElectricScooter, True),
    "2": ("Велосипед", Bicycle, False),
    "3": ("Электровелосипед", ElectricBike, True),
}
THING_TYPES = {
    "1": ("Шлем", Helmet, False),
    "2": ("Док-станция", DockStation, True),
    "3": ("Зарядный шкаф", ChargingCabinet, True),
}

MENU = """
=== ВышКат: учёт парка ===
1. Принять транспорт (с техосмотром)
2. Поставить вещь на баланс
3. Отчёт: число единиц и суммарная энергия
4. Транспорт для новичков
5. Инвентарная ведомость (техника и вещи)
6. Демо-сценарий
0. Выход"""


class ConsoleApp:
    def __init__(self, reception: ReceptionService, reports: FleetReports,
                 input_fn: Callable[[str], str] = input,
                 output_fn: Callable[[str], None] = print) -> None:
        self._reception = reception
        self._reports = reports
        self._input = input_fn
        self._print = output_fn

    # главный цикл 
    def run(self) -> None:
        actions = {
            "1": self._add_vehicle_dialog,
            "2": self._add_thing_dialog,
            "3": self.show_summary,
            "4": self.show_beginner_vehicles,
            "5": self.show_inventory,
            "6": self.run_demo,
        }
        try:
            while True:
                self._print(MENU)
                choice = self._input("Выберите пункт: ").strip()
                if choice == "0":
                    self._print("До встречи!")
                    return
                action = actions.get(choice)
                if action is None:
                    self._print("Нет такого пункта, попробуйте ещё раз.")
                    continue
                action()
        except (EOFError, KeyboardInterrupt):
            self._print("\nВвод завершён, выходим.")

    # диалоги 
    def _add_vehicle_dialog(self) -> None:
        _, cls, powered = self._choose_type(VEHICLE_TYPES, "Вид транспорта")
        model = self._ask_text("Модель: ")
        simplicity = self._ask_int("Простота для новичка (1-10): ", 1, 10)
        wear = self._ask_int("Износ, % (0-100): ", 0, 100)
        kwargs = {"model": model, "simplicity": simplicity, "wear_percent": wear}
        if powered:
            kwargs["daily_energy_kwh"] = self._ask_float("Суточный расход, кВт·ч: ")
        self.receive(cls(**kwargs))

    def _add_thing_dialog(self) -> None:
        _, cls, powered = self._choose_type(THING_TYPES, "Вид вещи")
        model = self._ask_text("Модель: ")
        if powered:
            thing = cls(model, self._ask_float("Суточный расход, кВт·ч: "))
        else:
            thing = cls(model)
        self.register(thing)

    # сценарии 
    def receive(self, vehicle) -> None:
        result = self._reception.receive_vehicle(vehicle)
        if result.accepted:
            self._print(f"[ПРИНЯТ] {vehicle.name} -> {vehicle.inventory_number}")
        else:
            self._print(f"[ОТКЛОНЁН] {vehicle.name}: {result.reason}")

    def register(self, thing) -> None:
        number = self._reception.register_thing(thing)
        self._print(f"[НА БАЛАНСЕ] {thing.name} -> {number}")

    def show_summary(self) -> None:
        self._print(f"Всего единиц на балансе: {self._reports.total_units()}")
        for kind, count in sorted(self._reports.units_by_kind().items()):
            self._print(f"  {kind}: {count}")
        self._print(f"Суммарный суточный расход: "
                    f"{self._reports.total_daily_energy_kwh():.2f} кВт·ч")

    def show_beginner_vehicles(self) -> None:
        vehicles = self._reports.beginner_vehicles()
        if not vehicles:
            self._print("Транспорта для новичков пока нет.")
            return
        self._print("Транспорт для новичков:")
        for v in vehicles:
            self._print(f"  {v.inventory_number}  {v.name} (простота {v.simplicity})")

    def show_inventory(self) -> None:
        rows = self._reports.inventory_list()
        if not rows:
            self._print("На балансе ничего нет.")
            return
        self._print("Инвентарная ведомость:")
        for number, name in rows:
            self._print(f"  {number}  {name}")

    def run_demo(self) -> None:
        self._print("\n--- Демо: приёмка транспорта ---")
        self.receive(ElectricScooter("Ninebot Max", simplicity=7, daily_energy_kwh=0.6))
        self.receive(ElectricScooter("Kugoo Turbo", simplicity=4, daily_energy_kwh=0.9))
        self.receive(Bicycle("Stels Navigator", simplicity=9))
        self.receive(ElectricBike("Eltreco XT", simplicity=6, daily_energy_kwh=1.2))
        self.receive(ElectricScooter("Старый самокат", simplicity=8,
                                     daily_energy_kwh=0.5, wear_percent=70))
        self.receive(ElectricBike("Прожорливый", simplicity=5, daily_energy_kwh=5.0))
        self._print("\n--- Демо: вещи на балансе ---")
        self.register(Helmet("ВышКат Kids"))
        self.register(DockStation("Док у корпуса на Покровке", daily_energy_kwh=2.5))
        self.register(ChargingCabinet("Шкаф №1", daily_energy_kwh=4.0))
        self._print("\n--- Демо: отчёты ---")
        self.show_summary()
        self.show_beginner_vehicles()
        self.show_inventory()

    # ввод с проверкой 
    def _choose_type(self, catalog: dict, title: str) -> tuple:
        for key, (label, _, _) in catalog.items():
            self._print(f"  {key}. {label}")
        while True:
            key = self._input(f"{title}: ").strip()
            if key in catalog:
                return catalog[key]
            self._print("Нет такого варианта.")

    def _ask_text(self, prompt: str) -> str:
        while True:
            value = self._input(prompt).strip()
            if value:
                return value
            self._print("Значение не может быть пустым.")

    def _ask_int(self, prompt: str, low: int, high: int) -> int:
        while True:
            raw = self._input(prompt).strip()
            if raw.lstrip("-").isdigit() and low <= int(raw) <= high:
                return int(raw)
            self._print(f"Введите целое число от {low} до {high}.")

    def _ask_float(self, prompt: str) -> float:
        while True:
            raw = self._input(prompt).strip().replace(",", ".")
            try:
                value = float(raw)
            except ValueError:
                value = -1.0
            if value >= 0:
                return value
            self._print("Введите неотрицательное число.")
