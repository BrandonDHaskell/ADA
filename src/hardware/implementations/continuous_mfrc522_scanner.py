import threading
import time
from src.hardware.interfaces.continuous_monitoring_interface import ContinuousMonitoringInterface

class RFIDContinuousMonitor(ContinuousMonitoringInterface):
    def __init__(self, config):
        self.monitoring_interval = config.get("monitoring_interval", 1)  # Default to 1 second
        self.shared_state = config.get("threading_shared_var")
        self.mfrc522_reader = config.get("mfrc522_reader")
        super().__init__(config)

        self.monitoring_thread = None
        self.running = False
        self.logger.info("RFIDContinuousMonitor initialized")

    def initialize(self):
        return super().initialize()
    
    def start_monitoring(self):
        if not self.running:
            self.running = True
            self.monitoring_thread = threading.Thread(target=self._monitor_rfid)
            self.monitoring_thread.start()
            self.logger.info("RFID monitoring started")

    def stop_monitoring(self):
        self.running = False
        if self.monitoring_thread:
            self.monitoring_thread.join()
            self.logger.info("RFID monitoring thread joined")

        # Call the cleanup method of MFRC522Reader
        if hasattr(self.mfrc522_reader, 'cleanup'):
            self.mfrc522_reader.cleanup()
            self.logger.debug("MFRC522 reader cleanup called")

    def _monitor_rfid(self):
        while self.running:
            rfid_id = self.mfrc522_reader.scan_for_obf_id()
            if rfid_id:
                self.shared_state.set(rfid_id)
                self.logger.debug(f"RFID ID scanned and set: {rfid_id}")
                # Optionally, add a break here if you want to stop monitoring after the first successful scan
            time.sleep(self.monitoring_interval)
        self.logger.info("RFID monitoring loop has stopped")