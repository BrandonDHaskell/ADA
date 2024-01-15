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

@pytest.mark.parametrize("common_to_ground, normally_open, gpio_high, expected_status", [
    (True, True, True, 'inactive'),
    (True, True, False, 'active'),
    (True, False, True, 'active'),
    (True, False, False, 'inactive'),
    (False, True, True, 'active'),
    (False, True, False, 'inactive'),
    (False, False, True, 'inactive'),
    (False, False, False, 'active'),
])

def test_pi_gpio_switch_reader(mock_gpio, common_to_ground, normally_open, gpio_high, expected_status):
    # Import mock RPi.GPIO for testing
    from src.hardware.implementations.pi_gpio_switch_reader import PiGPIOSwitchReader

    config = {
        "pin_number": 12,
        "normally_open": normally_open,
        "common_to_ground": common_to_ground
    }
    switch_reader = PiGPIOSwitchReader(config)
    switch_reader.initialize(config)

    mock_gpio.input.return_value = mock_gpio.HIGH if gpio_high else mock_gpio.LOW

    status = switch_reader.get_status()
    assert status == expected_status

    # Clean up if actually using GPIO pins
    switch_reader.cleanup()