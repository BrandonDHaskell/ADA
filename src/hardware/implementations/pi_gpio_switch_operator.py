import RPi.GPIO as GPIO
from src.hardware.interfaces.toggle_interface import ToggleOperatorInterface

class PiGPIOSwitchOperator(ToggleOperatorInterface):
    """
    A GPIO pin operator for controlling switches using a Raspberry Pi.
    This class allows setting a GPIO pin to a HIGH or LOW state.
    """

    def __init__(self, config):
        self.pin_number = config.get("pin_number")
        self.state = GPIO.LOW  # Default state
        super().__init__(config)
        
        self.initialize()

    def initialize(self):
        GPIO.setmode(GPIO.BCM)  # Use BCM numbering
        GPIO.setup(self.pin_number, GPIO.OUT)  # Set the pin to OUT mode
        self.logger.info(f"GPIO pin {self.pin_number} set to OUT mode.")

    def set_status(self, new_state):
        """
        Set the GPIO pin to the specified state: HIGH or LOW
        :param new_state: The new state to set the pin to HIGH or LOW, should be 'active' or 'inactive'
        """
        if new_state.lower() == "active":
            GPIO.output(self.pin_number, GPIO.HIGH)
            self.state = GPIO.HIGH
            self.logger.info(f"Set GPIO pin {self.pin_number} to HIGH (active).")
        elif new_state.lower() == "inactive":
            GPIO.output(self.pin_number, GPIO.LOW)
            self.state = GPIO.LOW
            self.logger.info(f"Set GPIO pin {self.pin_number} to LOW (inactive).")
        else:
            self.logger.error(f"Invalid state: {new_state}. State must be 'active' or 'inactive'.")

    def cleanup(self):
        """
        Clean up by resetting the GPIO pin.
        """
        # GPIO.cleanup(self.pin_number)
        self.logger.info(f"Cleaned up GPIO pin {self.pin_number}.")