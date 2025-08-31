import time
from config.settings import settings
from config.logging import log
from kafka_client.producer import fetch_and_send


def main() -> None:    
    log.info("Producer start: topic=%s, bootstrap=%s", settings.KAFKA_TOPIC, settings.KAFKA_BOOTSTRAP_SERVERS)
    
    while True:
        try:
            sent = fetch_and_send()
            log.info("fetch and sned done: sent=%d", sent)
        except Exception:
            log.exception("Cycle failed")
        time.sleep(2)
    

if __name__ == "__main__":
    main()
