import signal
import sys
from default_logger import default_logger


def interrupt_handler():
    signal.signal(signal.SIGINT, sigint_handler)


def sigint_handler(signal, frame):
    log = default_logger()
    print('\nKeyboardInterrupt is caught, exiting...')
    log.debug('KeyboardInterrupt is caught, exiting...')
    sys.exit(0)
