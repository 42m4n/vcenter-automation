from loguru import logger
import logging


class DjangoLogHandler(logging.Handler):
    def emit(self, record):
        try:
            msg = self.format(record)
            level_name = logging.getLevelName(record.levelno)
            logger.opt(depth=1, exception=None).log(level_name, msg)
        except Exception:
            self.handleError(record)


log_format = "<green>{time:YYYY-MM-DD--HH:mm:ss}</green> [{level}] - [{name} > {function}() > {line}] - {message}"

# Add the custom handler to Django's logging configuration
logging.basicConfig(handlers=[DjangoLogHandler()], level=logging.INFO)

# Configure Loguru to write logs to files with rotation
logger.add("logs/{time:YYYY-MM-DD--HH-DD}.log", format=log_format, rotation="1 day", level="INFO")
