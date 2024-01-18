import threading
import time
from src.hardware.interfaces.toggle_monitoring_interface import ToggleMonitoringInterface

class ContinuousSwitchMonitor(ToggleMonitoringInterface):
    def __init__(self, config, switch_reader):
        super().__init__(config)
        self.switch_reader = switch_reader

        # Extract monitoring interval from config, with a default value
        self.monitoring_interval = config.get("monitoring_interval", 1)  # Default to 1 second

        self.monitoring_thread = None
        self.running = False

    def initialize(self):
        self.switch_reader.initialize()

    def start_monitoring(self):
        if not self.running:
            self.running = True
            self.monitoring_thread = threading.Thread(target=self._monitor_switch)
            self.monitoring_thread.start()

    def stop_monitoring(self):
        self.running = False
        if self.monitoring_thread:
            self.monitoring_thread.join()
        self.switch_reader.cleanup()

    def _read_current_state(self):
        return self.switch_reader.get_status()

    def _monitor_switch(self):
        while self.running:
            self.update_shared_state()  # Updates the shared state if there's a change
            time.sleep(self.monitoring_interval)  # Sleep for the specified interval