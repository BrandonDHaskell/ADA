import logging
import time
class MillisecondFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = time.strftime(datefmt, ct)
            return f"{s}.{int(record.msecs):03d}"
        else:
            return super().formatTime(record, datefmt)

def setup_logging(level="INFO"):
    logging.basicConfig(level=level)
    formatter = MillisecondFormatter(fmt="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
    
    # Apply the formatter to all handlers
    for handler in logging.root.handlers:
        handler.setFormatter(formatter)