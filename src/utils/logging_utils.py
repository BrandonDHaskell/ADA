import logging
import time

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

def setup_logging(level="INFO"):
    """
    Sets up logging for the application with an optional log level.
    :param level: The logging level, e.g., logging.DEBUG, logging.INFO, etc.
                  Defaults to logging.INFO if none is provided.
    """
    if level is None:
        level = logging.INFO
        
    logging.basicConfig(level=level)
    formatter = MillisecondFormatter(fmt="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
    
    # Apply the formatter to all handlers
    for handler in logging.root.handlers:
        handler.setFormatter(formatter)