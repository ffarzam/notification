import threading

from listener import start_consumers
from config.config import get_settings

settings = get_settings()


def start_listeners():
    for item in settings.QUEUE_NAME_LIST:
        threading.Thread(target=start_consumers, args=[item]).start()


if __name__ == "__main__":
    start_listeners()
