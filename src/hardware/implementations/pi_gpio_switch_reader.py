import logging
import RPi.GPIO as GPIO
from src.hardware.interfaces.toggle_interface import ToggleReaderInterface

class PiGPIOSwitchReader(ToggleReaderInterface):
    """
    A generic GPIO pin reader for implementing switch status retrievals for ADA.
    Depending on different hardware implentations, switch readings might vary.
    GPIOSwitchReader is configurable for Normally Open (NO) or Normally Closed (NC)
    switches as well as wiring which is either common to ground or to power.

    The default setting is NO & Common to Ground.
    Output of GPIOSwitchReader is as follows:
        +-------------------+----------+---------------------------+
        | Common to Ground  |    NO    |     Pin Return Mapping    |
        +-------------------+----------+---------------------------+
        |       True        |   True   | HIGH=inactive, LOW=active |
        |       True        |   False  | HIGH=active, LOW=inactive |
        |       False       |   True   | HIGH=active, LOW=inactive |
        |       False       |   False  | HIGH=inactive, LOW=active |
        +-------------------+----------+---------------------------+
    """
    def __init__(self, config_info):
        # Set defaults for normally_open and common_to_ground
        self.normally_open = config_info.get("normally_open", True)
        self.common_to_ground = config_info.get("common_to_ground", True )
        super().__init__(config_info)
        self.logger = logging.getLogger(__name__)
        self.pin_number = config_info["pin_number"] # Assumes pin_number is provided (TODO - add error checking)
        self.logger.info(f"Initializing PiGPIOSwitchReader: pin_number={self.pin_number}, normally_open={self.normally_open}, common_to_ground={self.common_to_ground}")

    def initialize(self, config_info):
        GPIO.setmode(GPIO.BCM)  # BCM numbering
        # Setup GPIO pin with pull-up or pull-down based on common_to_ground
        if self.common_to_ground:
            GPIO.setup(self.pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        else:
            GPIO.setup(self.pin_number, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def get_status(self):
        pin_state = GPIO.input(self.pin_number)
        # Determines status based on normally_open configuration
        if self.normally_open:
            status = "inactive" if pin_state == GPIO.HIGH else "active"
        else:
            status = "active" if pin_state == GPIO.HIGH else "inactive"
        self.logger.info(f"Read status from pin {self.pin_number}: {status}")
        return status
        
    def cleanup(self):
        GPIO.cleanup(self.pin_number)