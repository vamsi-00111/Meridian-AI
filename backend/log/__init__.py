from .logger import Customlog

# Create a single shared logger instance
_LOGGER_INSTANCE = Customlog()
GLOBAL_LOGGER = _LOGGER_INSTANCE.get_logger("MeridianAI_Backend")