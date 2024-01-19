import logging
import time
from pathlib import Path

# Adds milliseconds to the timestamp output in logging
class MillisecondFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = time.strftime(datefmt, ct)
            return f"{s}.{int(record.msecs):03d}"
        else:
            return super().formatTime(record, datefmt)
    
    # Override name formatter to only the module name
    def format(self, record):
        # Shorten the logger's name to the last component
        # record.name = record.name.split('.')[-1] # not needed if using ada_interface
        return super(MillisecondFormatter, self).format(record)

def setup_logging(level=None):
    """
    Sets up logging for the application with an optional log level.
    :param level: The logging level, e.g., logging.DEBUG, logging.INFO, etc.
                  Defaults to logging.INFO if none is provided.
    """
    if level is None:
        level = logging.INFO

    logger = logging.getLogger()
    if not logger.handlers:  # Check if handlers already exist
        # Define log file path
        script_directory = Path(__file__).resolve().parent.parent.parent
        log_directory = script_directory / "logs"
        log_directory.mkdir(parents=True, exist_ok=True)
        log_file_path = log_directory / "ada.log"

        # Create file handler
        file_handler = logging.FileHandler(log_file_path)
        console_handler = logging.StreamHandler()  # For console output

        # Create formatter and add it to handlers
        formatter = MillisecondFormatter(fmt="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        # Set the logging level
        logger.setLevel(level)