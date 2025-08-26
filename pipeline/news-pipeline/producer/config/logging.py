import logging

def setup_logging(level: str = "INFO") -> None:
    log = logging.getLogger("producer")
    log.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )
    return log

log = setup_logging()
