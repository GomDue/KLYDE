import time
from config.settings import settings
from config.logging import setup_logging
from kafka_client.producer import fetch_and_send


def main() -> None:
    setup_logging(settings.LOG_LEVEL)
    
    while True:
        fetch_and_send()
        time.sleep(2)
    

if __name__ == "__main__":
    main()
