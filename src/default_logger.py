import os
import logging
from logging.handlers import RotatingFileHandler


def default_logger():
    """Default logging configuration for functions which cannot load the configuration file.
    """
    log_level = 'DEBUG'
    log_file_path = ''
    if os.name == 'nt':
        # Set DATA directory for Windows systems
        data_directory = 'C:/ProgramData/pyModSync'
        # Set log file path for Windows systems
        log_file_path = data_directory + '/pymodsync.log'
    # If not, hope for linux system
    else:
        # Set log path by expanding user home path from ~
        user_home = os.path.expanduser("~")
        data_directory = user_home + '/.cache/pyModSync'
        log_file_path = data_directory + '/pymodsync.log'
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)
    # Log config
    # 'a' for append, 'w' for write
    log_write_mode = 'a'
    # Max filesize before rotating in bytes
    log_rotate_max_size = 5120000
    # Max file count
    log_rotate_max_files = 4

    handlers = [
        RotatingFileHandler(filename=log_file_path, mode=log_write_mode,
                            maxBytes=log_rotate_max_size, backupCount=log_rotate_max_files)
            ]

    # Set date format of logs to yyyy-mm-dd hh:mm:ss
    data_format = '%Y-%m-%d %H:%M:%S'
    # Set log format to 'DATE_FORMAT.fff - [LOG_LEVEL] - LOG_MESSAGE
    log_format = '%(asctime)s.%(msecs)03d - [%(levelname)s] - %(message)s'

    logging.basicConfig(handlers=handlers, level=log_level, format=log_format, datefmt=data_format)

    return logging.getLogger('pymodsync_logger')
