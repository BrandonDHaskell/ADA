import threading
import time
from src.hardware.interfaces.toggle_monitoring_interface import ToggleMonitoringInterface

class ContinuousSwitchMonitor(ToggleMonitoringInterface):
    def __init__(self, config):
        # Extract monitoring interval from config, with a default value
        self.monitoring_interval = config.get("monitoring_interval", 1)  # Default to 1 second
        self.shared_state = config.get("threading_shared_var")
        self.switch_reader = config.get("switch_reader")
        self.last_state = None
        super().__init__(config)

        # Validate 
        if self.shared_state is None:
            raise ValueError("threading_shared_var must be provided in the config")
        if self.switch_reader is None:
            raise ValueError("switch_reader must be provided in the config")

        self.monitoring_thread = None
        self.running = False
        self.logger.info("ContinuousSwitchMonitor initialized")
        self.switch_reader.initialize()

    def initialize(self):
        self.switch_reader.initialize()

    def start_monitoring(self):
        if not self.running:
            self.running = True
            self.monitoring_thread = threading.Thread(target=self._monitor_switch)
            self.monitoring_thread.start()
            self.logger.info("Switch monitoring started")

    def stop_monitoring(self):
        self.running = False
        if self.monitoring_thread:
            self.monitoring_thread.join()
            self.logger.info("Switch monitoring stopped")
        self.switch_reader.cleanup()

    def _read_current_state(self):
        return self.switch_reader.get_status()

    def _monitor_switch(self):
        while self.running:
            current_state = self._read_current_state()
            if current_state != self.last_state:
                self.shared_state.set(current_state)
                self.logger.debug(f"Switch state changed from {self.last_state} to {current_state}")
                self.last_state = current_state  # Update the last state
            time.sleep(self.monitoring_interval)