import pytest
from unittest.mock import Mock, patch
from src.hardware.implementations.pi_gpio_switch_operator import PiGPIOSwitchOperator

@pytest.fixture
def mock_gpio():
    with patch("src.hardware.implementations.pi_gpio_switch_operator.GPIO") as mock_gpio:
        yield mock_gpio