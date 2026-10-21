from vyshkat.console import ConsoleApp
from vyshkat.container import build_container
from vyshkat.services.fleet import Fleet
from vyshkat.services.reception import ReceptionService
from vyshkat.services.reports import FleetReports


def make_app(inputs):
    container = build_container()
    lines = []
    feed = iter(inputs)

    def fake_input(_prompt):
        try:
            return next(feed)
        except StopIteration:
            raise EOFError from None

    app = ConsoleApp(container.resolve(ReceptionService), container.resolve(FleetReports),
                     input_fn=fake_input, output_fn=lines.append)
    return app, container, lines


def test_demo_shows_accept_reject_and_reports():
    app, container, lines = make_app([])
    app.run_demo()
    text = "\n".join(lines)
    assert "[ПРИНЯТ]" in text and "[ОТКЛОНЁН]" in text
    assert "Суммарный суточный расход" in text
    assert "Транспорт для новичков" in text
    assert len(container.resolve(Fleet).items()) == 7


def test_interactive_add_vehicle_with_bad_input_then_reports():
    inputs = [
        "1", "9", "1", "", "Ninebot", "abc", "7", "10", "-1", "0.6",  # самокат, с ошибками ввода
        "2", "2", "Док", "1,5",                                      # док-станция
        "2", "1", "Шлем-1",                                          # шлем
        "3", "4", "5", "x", "0",
    ]
    app, container, lines = make_app(inputs)
    app.run()
    text = "\n".join(lines)
    assert "[ПРИНЯТ] Электросамокат «Ninebot» -> VK-0001" in text
    assert "Суммарный суточный расход: 2.10 кВт·ч" in text
    assert "VK-0003  Шлем «Шлем-1»" in text
    assert "Нет такого пункта" in text
    assert text.endswith("До встречи!")


def test_empty_reports_and_eof_exit():
    app, _, lines = make_app(["4", "5"])
    app.run()  # после двух команд ввод заканчивается -> EOF, выходим без ошибки
    text = "\n".join(lines)
    assert "Транспорта для новичков пока нет." in text
    assert "На балансе ничего нет." in text
