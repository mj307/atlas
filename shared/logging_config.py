import logging
import structlog
'''
### `shared/logging_config.py` — `setup_logging`, `get_logger`
`setup_logging(service_name, log_level)` configures structlog with JSON output.
`get_logger(name)` returns a bound structlog logger.  Called once at module import time
in each service's `main.py`.
'''

def setup_logging(service_name: str, log_level: str):
    logging.basicConfig(level=log_level)
    
    structlog.configure(
        processors=[structlog.processors.TimeStamper(fmt='iso'),
                    structlog.processors.add_log_level,
                    structlog.processors.JSONRenderer]    
    )

def get_logger(name):
    return structlog.get_logger(name) # old way is logging.getLogger(name)
    
    





