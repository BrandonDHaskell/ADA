import pytest
from unittest.mock import MagicMock

# Mock RPi.GPIO before importing PiGPIOSwitchReader
pytest.importorskip("RPi.GPIO")
@pytest.fixture(scope="module", autouse=True)
def mock_rpi_gpio(mocker):
    rpi_gpio_mock = MagicMock()
    modules = {
        "RPi": MagicMock(),
        "RPi.GPIO": rpi_gpio_mock
    }
    with pytest.MonkeyPatch().context() as m:
        m.setattr("sys.modules", modules)
        yield rpi_gpio_mock

from src.hardware.implementations.pi_gpio_switch_operator import PiGPIOSwitchOperator

def test_initialize(rpi_gpio_mock):
    config = {"pin_number": 17}
    operator = PiGPIOSwitchOperator(config)
    operator.initialize()

    rpi_gpio_mock.setmode.assert_called_with(rpi_gpio_mock.BCM)
    rpi_gpio_mock.setup.assert_called_with(17, rpi_gpio_mock.OUT)

def test_set_status_high(rpi_gpio_mock):
    config = {"pin_number": 17}
    operator = PiGPIOSwitchOperator(config)
    operator.initialize()
    operator.set_status("HIGH")

    rpi_gpio_mock.output.assert_called_with(17, rpi_gpio_mock.HIGH)