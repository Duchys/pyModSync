import logging
from logging.handlers import RotatingFileHandler
from config_manager import check_if_config_exists
from config_manager import config_loader


def load_log_config():
    """Load log level and path config, otherwise return default values
    """
    # Check if config already exists, if not, create it
    check_if_config_exists()

    # Load log configuration
    config = config_loader()
    log_level = config[7]
    log_file_path = config[8]
    # Return loaded values
    return [log_level, log_file_path]


def logger():
    """Configure logging for the entire application
    """
    # Call log config loader and save returned values to variables
    log_config = load_log_config()
    log_level = log_config[0]
    log_file_path = log_config[1]

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
