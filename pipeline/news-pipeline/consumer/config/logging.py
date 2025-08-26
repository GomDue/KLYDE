import logging
from config.settings import settings

def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )

    logging.FileHandler(settings.LOG_PATH, encoding="utf-8")
    return logging.getLogger("consumer")

log = setup_logging()
