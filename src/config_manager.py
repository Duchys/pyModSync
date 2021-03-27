import configparser
import os
import logging
import sys
import traceback
from logging.handlers import RotatingFileHandler
import requests


# Setup logging
# Log level (options: CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET)
LOG_LEVEL = 'DEBUG'
# 'a' for append, 'w' for write
LOG_WRITE_MODE = 'a'
# Max filesize before rotating in bytes
LOG_ROTATE_MAX_SIZE = 5120000
# Max file count
LOG_ROTATE_MAX_FILES = 4
# Check if Windows is used
if os.name == 'nt':
    # Set DATA directory for Windows systems
    DATA_DIRECTORY = 'C:/ProgramData/pyModSync'
    CONFIG_DIRECTORY = DATA_DIRECTORY + '/cfg'
    # Set Config directory for Windows systems
    CONFIG_LOCATION = CONFIG_DIRECTORY + '/pymodsync.properties'
    # Set log file path for Windows systems
    LOG_FILE_PATH = DATA_DIRECTORY + '/pymodsync.log'
# If not, hope for linux system
else:
    # Set log path by expanding user home path from ~
    USER_HOME = os.path.expanduser("~")
    DATA_DIRECTORY = USER_HOME + '/.cache/pyModSync'
    CONFIG_DIRECTORY = USER_HOME + '/.config/pyModSync'
    CONFIG_LOCATION = CONFIG_DIRECTORY + '/pymodsync.properties'
    LOG_FILE_PATH = DATA_DIRECTORY + '/pymodsync.log'

# Create log directory for log files
if not os.path.exists(DATA_DIRECTORY):
    os.makedirs(DATA_DIRECTORY)
    print('Data Directory created in %s', DATA_DIRECTORY)


# Log handlers
# Filename = place where to store the logs
# mode = sets appending or overwriting of log files
# maxBytes = log rotating after set filesize
# backupCount = 4 number of files to keep


handlers = [
    RotatingFileHandler(filename=LOG_FILE_PATH, mode=LOG_WRITE_MODE,
                        maxBytes=LOG_ROTATE_MAX_SIZE, backupCount=LOG_ROTATE_MAX_FILES)
           ]

# Set date format of logs to yyyy-mm-dd hh:mm:ss
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
# Set log format to 'DATE_FORMAT.fff - [LOG_LEVEL] - LOG_MESSAGE
LOG_FORMAT = '%(asctime)s.%(msecs)03d - [%(levelname)s] - %(message)s'

logging.basicConfig(handlers=handlers, level=LOG_LEVEL, format=LOG_FORMAT, datefmt=DATE_FORMAT)


def check_if_config_exists():
    """Checks if the configration file is already created
    """
    # Check if data directory for program files exists
    log = logging.getLogger('default_logger')

    if not os.path.exists(DATA_DIRECTORY):
        os.makedirs(DATA_DIRECTORY)
        log.info('%s does not exist, creating directories', DATA_DIRECTORY)
        log.info('Log directory created in %s', DATA_DIRECTORY)
    else:
        log.info('%s exists...', DATA_DIRECTORY)

    log = logging.getLogger('default_logger')

    log.info('checking if configuration file exists')
    # Check if config file exists
    if os.path.isfile(CONFIG_LOCATION):
        log.info('Config file found')
        print('Configuration file found, loading configuration...')
        return 1

    log.info('No config file found')
    # Calling create config fuction
    log.debug('Calling create_config fuction.')
    create_config()
    return 0


def read_steam_registry(steam_reg_location):
    """Read Steam key registry for install path location and verify it
    """
    # Winreg is imported in here instead of top level, as it would otherwise crash the program on Linux Systems
    import winreg  # pylint: disable=import-error,import-outside-toplevel
    log = logging.getLogger('default_logger')
    log.info('Opening 64-bit Steam registry key')
    print('Opening 64-bit Steam registry key')
    # Open 64-bit steam registry key
    steam_reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, steam_reg_location)
    # Read values from InstallPath
    steam_exe_path = winreg.QueryValueEx(steam_reg_key, "InstallPath")
    # Add steam.exe to the install path fo steam
    steam_exe_path = str(steam_exe_path[0]) + "\\steam.exe"
    # Toss a exception if path is not found
    log.info('Checking if steam.exe path value from registry is valid')
    if os.path.isfile(steam_exe_path):
        log.info('Steam path from registry is valid')
        return steam_exe_path
    log.warning('Steam path from registry is invalid')
    raise FileNotFoundError(f'{steam_exe_path} not found') from FileNotFoundError


def ask_if_steam_is_installed():
    """Ask user if steam is installed.
    """
    log = logging.getLogger('default_logger')
    steam_installed = input('Is steam installed? [YES/no]') or 'yes'
    steam_installed = steam_installed.lower()
    log.info('User responded %s', steam_installed)
    return steam_installed


def ask_for_steam_path():
    """Ask user for steam path
    """
    log = logging.getLogger('default_logger')
    steam_exe_path = input('Please enter path to the steam.exe (ie. C:\\Steam\\steam.exe)')
    log.info('User responded %s', steam_exe_path)
    return steam_exe_path


def steam_path_requester():
    """Ask user for steam path and validate it.
    """
    log = logging.getLogger('default_logger')
    print('Path to steam not found in registry')
    log.info('Path to steam not found in registry')
    log.info('Asking user if steam is installed')
    # Ask user if steam is installed
    steam_installed = ask_if_steam_is_installed()
    # Check if users response is valid
    while steam_installed not in ('yes', 'y', 'no', 'n'):
        # if not, ask again
        log.warning('Invalid entry provided, asking the user if steam is installed again')
        print('Invalid entry, valid entries are YES, NO, N, Y')
        steam_installed = ask_if_steam_is_installed()
    while steam_installed in ('yes', 'y'):
        # If user responded that steam is installed, ask him for path to steam
        log.info('Asking user for path to steam.exe')
        steam_exe_path = ask_for_steam_path()
        # Check if provided path ends in file and if steam is installed
        while not os.path.isfile(steam_exe_path) and steam_installed in ('yes', 'y'):
            log.warning('Invalid entry provided, asking the user for path to steam.exe again')
            print('Invalid path provided.')
            # Ask user if steam is really installed
            steam_installed = ask_if_steam_is_installed()
            # Check validity of answer
            while steam_installed not in ('yes', 'y', 'no', 'n'):
                # if not, ask again
                log.warning('Invalid entry provided, asking the user if steam is installed again')
                print('Invalid entry, valid entries are YES, NO, N, Y')
                steam_installed = ask_if_steam_is_installed()
            if steam_installed in ('yes', 'y'):
                # Ask user for path to steam.exe
                steam_exe_path = ask_for_steam_path()
        if steam_installed in ('yes', 'y'):
            return steam_exe_path
    steam_exe_path = ''
    return steam_exe_path


def ask_for_arma_path():
    """Ask user for path to arma3.exe
    """
    log = logging.getLogger('default_logger')
    arma_exe_path = input('Please enter path to your arma3.exe (ie. C:\\Arma3\\arma3.exe)')
    log.info('User responded %s', arma_exe_path)
    return arma_exe_path


def arma_path_requester():
    """Ask user for path to arma3.exe and validate it
    """

    log = logging.getLogger('default_logger')
    log.info('Asking the user for path to arma3.exe')
    # Ask user for path to arma3.exe
    arma_exe_path = ask_for_arma_path()
    while arma_exe_path == '':
        log.warning('No entry provided, asking the user for path to arma3.exe again')
        print('No path provided, please provide a path.')
        arma_exe_path = ask_for_arma_path()
    while not os.path.isfile(arma_exe_path):
        log.warning('Invalid entry provided, asking the user for path to arma3.exe again')
        print('Invalid path provided, please provide correct path.')
        arma_exe_path = ask_for_arma_path()
        log.info('Arma3 path is a file')
    return arma_exe_path


def game_path_requester():
    """Finds to path to the steam.exe or arma.exe from registry or user input
    """
    log = logging.getLogger('default_logger')

    log.info('Reading registry for steam path')
    arma_exe_path = ''
    steam_exe_path = ''

    try:
        # Registry keys for steam install location
        steam_reg_location_32bit = "SOFTWARE\\Valve\\Steam"
        steam_reg_location_64bit = "SOFTWARE\\WOW6432Node\\Valve\\Steam"
        try:
            steam_exe_path = read_steam_registry(steam_reg_location_64bit)
            return [steam_exe_path, arma_exe_path]
        except (OSError, FileNotFoundError, EnvironmentError) as err:
            try:
                log.debug(err)
                steam_exe_path = read_steam_registry(steam_reg_location_32bit)
                return [steam_exe_path, arma_exe_path]
            except (OSError, FileNotFoundError, EnvironmentError) as err:
                log.debug(err)
                steam_exe_path = steam_path_requester()
                if steam_exe_path != '':
                    return [steam_exe_path, arma_exe_path]
                arma_exe_path = arma_path_requester()
                return [steam_exe_path, arma_exe_path]

    # Raise exception if all else fails
    except (OSError, EnvironmentError):
        print('Unhandled exception located, report steps taken to application author')
        print('Exiting...')
        log.error('Unhandled exception located, report steps taken to application author')
        log.error('Exiting...')
        trace_back = traceback.format_exc()
        log.error(trace_back)
        print(trace_back)
        sys.exit()


def local_addon_path_requester():
    """Ask user for local addon path and verify it, if it does not exist create it.
    """
    log = logging.getLogger('default_logger')

    def ask_for_local_addon_path():
        """Ask user for local addon path.
        """
        if os.name == 'nt':
            local_addon_path = input('Please enter path to your local addon directory (ie. C:\\417addons): ')
        else:
            local_addon_path = input('Please enter path to your local addon directory (ie. /opt/Arma3addons): ')
        log.info('User submitted %s', local_addon_path)
        return local_addon_path

    print('No configuration file found...')
    log.info('Asking user for path to local addon directory')
    print('Do not use the arma !WORKSHOP directory')
    print('If path does not exist, it will be created')
    local_addon_path = ask_for_local_addon_path()
    # Check if path was provided
    while local_addon_path == '':
        print('No addon path provided')
        log.warning('No addon path was provided, asking user again')
        local_addon_path = ask_for_local_addon_path()
    # Check if path is file
    while os.path.isfile(local_addon_path):
        log.warning('Path exists but point to file, asking user again')
        print('Path exists but points to file, please enter valid path')
        local_addon_path = ask_for_local_addon_path()
    # Check if path exists
    if not os.path.isdir(local_addon_path) and not os.path.isfile(local_addon_path):
        print('Directory not found, creating the path.')
        log.info('Valid path provided, creating path')
        # Try to create the path
        try:
            os.makedirs(local_addon_path)
            print(f'{local_addon_path} created')
            log.info('%s path created', local_addon_path)

            # Remove leading / from the path if present
            log.debug('Checking if leading slash is present')
            if local_addon_path.endswith('/'):
                local_addon_path = local_addon_path[:-1]
            log.debug('Leading slash removed from path')

            return local_addon_path
        except OSError:
            print('OSError exception located.')
            print('Exiting...')
            trace_back = traceback.format_exc()
            log.error(trace_back)
            print(trace_back)
            sys.exit()
    else:
        log.info('Provided path is valid, path is present.')
        print('Provided path is valid, path is present.')

        # Remove leading / from the path if present
        log.debug('Checking if leading slash is present')
        if local_addon_path.endswith('/'):
            local_addon_path = local_addon_path[:-1]
        log.debug('Leading slash removed from path')

        return local_addon_path


def remote_repository_url_requester():
    """Ask user for remote repostiory url and verify if it is available.
    """
    log = logging.getLogger('default_logger')

    def ask_for_remote_repository_url():
        """Ask the user for remote repository url.
        """
        remote_repository_url = input('Please enter URL of the remote repository (ie. https://franta.com/repo.csv): ')
        log.info('%s provided as URL of remote repository', remote_repository_url)
        return remote_repository_url

    # Asking user for URL to remote repository
    log.info('Asking user for URL of remote repository')
    remote_repository_url = ask_for_remote_repository_url()
    # Check anything was provided
    while remote_repository_url == '':
        print('No url was provided, please provide a URL')
        log.info('No URL was provided')
        remote_repository_url = ask_for_remote_repository_url()
        # Check status code of the remote repository
    try:
        log.info('Checking if the remote URL is reachable')
        repo_status = False
        while repo_status is False:
            try:
                repo_check_status_code = requests.head(remote_repository_url, timeout=15).status_code
            except (requests.exceptions.ConnectionError,
                    requests.exceptions.RequestException,
                    requests.exceptions.Timeout):
                # Set to status code if site is not reachable 451
                repo_check_status_code = 451

            if repo_check_status_code != 200:
                # Code did not match 200, asking for new URL
                print('Received non 200 status code')
                log.warning('Received non 200 status code')
                log.warning('Received %s status code', repo_check_status_code)
                print(f'Received {repo_check_status_code} status code')
                print('Please provide valid and reachable URL')
                log.info('Asking user to provide valid URL')
                # Asking user for new URL
                remote_repository_url = ask_for_remote_repository_url()
                # Checking if URL is not empty
                while remote_repository_url == '':
                    print('No URL was provided, please provide a URL')
                    log.info('No URL was provided')
                    # Asking user for new URL
                    remote_repository_url = ask_for_remote_repository_url()
            else:
                log.info('%s returned status code 200, continuing')
                repo_status = True
                return remote_repository_url
    except (requests.exceptions.ConnectionError,
            requests.exceptions.RequestException,
            requests.exceptions.Timeout) as err:
        print(f"URL {remote_repository_url} not reachable")
        log.error(err)
        sys.exit()


def create_config():
    """Generates config file on the initial start of the application
    """
    log = logging.getLogger('default_logger')
    config = configparser.ConfigParser(allow_no_value=True)

    # Check if data directory for program files exists
    print('Checking if %s directory exists', DATA_DIRECTORY)
    if not os.path.exists(DATA_DIRECTORY):
        log.info('%sdoes not exist, creating directories', DATA_DIRECTORY)
        os.makedirs(DATA_DIRECTORY)
        log.info('Log directory created in %s', DATA_DIRECTORY)

    # If the OS is windows
    log.debug('Checking system type.')
    if os.name == 'nt':
        log.debug('Windows system detected.')
        log.info('Creating configuration for Windows Systems')

        # Call game_path_requester function for getting path to steam or arma
        game_path = game_path_requester()
        steam_exe_path = game_path[0]
        arma_exe_path = game_path[1]
        # Replace \\ for /
        steam_exe_path = steam_exe_path.replace('\\', '/')
        arma_exe_path = arma_exe_path.replace('\\', '/')
    else:
        log.debug('Linux system detected.')
        log.info('Creating configuration for Linux Systems')

    remote_repository_destination_path = DATA_DIRECTORY + '/remoterepository.csv'
    local_repository = DATA_DIRECTORY + '/localrepo.csv'
    repository_difference_outfile = DATA_DIRECTORY + '/repodiffoutfile.csv'
    # Replace \\ for / in order to keep the formating the same in the entire configuration
    local_addon_path = local_addon_path_requester()
    remote_repository_url = remote_repository_url_requester()

    # Log set file locations, and paths
    log.info('Setting remote repostiory path to %s', remote_repository_destination_path)
    log.info('Setting local repostiory path to %s', local_repository)
    log.info('Setting repository difference path to %s', repository_difference_outfile)
    log.info('Setting remote repository url to %s', remote_repository_url)
    log.info('Setting local addon path to %s', local_addon_path)
    # Log this only for Windows systems
    if os.name == 'nt':
        log.info('Setting Arma3.exe path to %s', arma_exe_path)
        log.info('Setting Steam.exe path to %s', steam_exe_path)

    # Log set log configuration (this does not affect this file)
    log.info('Setting Log file path to %s', LOG_FILE_PATH)
    log.info('Setting Log level to %s', LOG_LEVEL)

    # Prepare config
    config['GENERAL'] = {}
    config['GENERAL']['# URL where the remote repository is available'] = None
    config['GENERAL']['remote_repository_url'] = remote_repository_url
    config['GENERAL']['# Destination path for remote checksum repository'] = None
    config['GENERAL']['remote_repository_destination_path'] = remote_repository_destination_path
    config['GENERAL']['# Addon folder location'] = None
    config['GENERAL']['local_addon_path'] = local_addon_path
    config['GENERAL']['# Destination path for the local checksum repository'] = None
    config['GENERAL']['local_repository'] = local_repository
    config['GENERAL']['# Destinaton path for the checksum comparison file'] = None
    config['GENERAL']['repository_difference_outfile'] = repository_difference_outfile

    # Windows specific config
    if os.name == 'nt':
        config['GENERAL']['# Path to steam.exe file, if empty, Arma3 is launched through Arma3 executable'] = None
        config['GENERAL']['steam_exe_path'] = steam_exe_path
        config['GENERAL']['# Path to arma3.exe file, if empty, Arma3 is launched through Steam'] = None
        config['GENERAL']['arma_exe_path'] = arma_exe_path

    # Logging config
    config['LOGGING'] = {}
    config['LOGGING']['# Log file destination path'] = None
    config['LOGGING']['log_file_path'] = LOG_FILE_PATH
    config['LOGGING']['Set logging level (Options: INFO, WARN, ERROR, DEBUG'] = None
    config['LOGGING']['log_level'] = LOG_LEVEL

    # Check if config directory for program files exists
    if not os.path.exists(CONFIG_DIRECTORY):
        log.info('%sdoes not exist, creating directories', CONFIG_DIRECTORY)
        os.makedirs(CONFIG_DIRECTORY)
    # Write config to file
    with open(CONFIG_LOCATION, 'w') as configfile:
        config.write(configfile)
    log.info('Config created')
    print('Config created')


def config_loader():
    """Loads the configuration file and returns the values as variables
    """
    log = logging.getLogger('default_logger')
    log.info('Loading configuration')
    config = configparser.ConfigParser()
    if os.name == 'nt':
        log.info('Windows system detected')
        # Path to config file
        config_location = 'C:/ProgramData/pyModSync/pymodsync.properties'
        # Reads the config file
        log.info('Reading configuration from %s', config_location)
        config.read(config_location)
        print(f'Loading configuration from {config_location}')
        # Saves contents of config file to variables
        remote_repository_url = config['GENERAL']['remote_repository_url']
        local_repository = config['GENERAL']['local_repository']
        repository_difference_outfile = config['GENERAL']['repository_difference_outfile']
        remote_repository_destination_path = config['GENERAL']['remote_repository_destination_path']
        local_addon_path = config['GENERAL']['local_addon_path']
        steam_exe_path = config['GENERAL']['steam_exe_path']
        arma_exe_path = config['GENERAL']['arma_exe_path']
        log_level = config['LOGGING']['log_level']
        log_file_path = config['LOGGING']['log_file_path']

        log.info('Loaded remote repository URL: %s', remote_repository_url)
        log.info('Loaded local repository path: %s', local_repository)
        log.info('Loaded repository difference outfile path: %s', repository_difference_outfile)
        log.info('Loaded remote repository destination path: %s', remote_repository_destination_path)
        log.info('Loaded steam.exe path: %s', steam_exe_path)
        log.info('Loaded arma3.exe path: %s', arma_exe_path)
        log.info('Loaded log level: %s', log_level)
        log.info('Loaded log file path: %s', log_file_path)

        return [remote_repository_url, local_repository, repository_difference_outfile,
                remote_repository_destination_path, local_addon_path, steam_exe_path,
                arma_exe_path, log_level, log_file_path]

    # Path to config file
    config_location = USER_HOME + '/.config/pyModSync/pymodsync.properties'
    # Reads the config file
    config.read(config_location)
    # Saves contents of config file to variables
    remote_repository_url = config['GENERAL']['remote_repository_url']
    local_repository = config['GENERAL']['local_repository']
    repository_difference_outfile = config['GENERAL']['repository_difference_outfile']
    remote_repository_destination_path = config['GENERAL']['remote_repository_destination_path']
    local_addon_path = config['GENERAL']['local_addon_path']
    log_level = config['LOGGING']['log_level']
    log_file_path = config['LOGGING']['log_file_path']

    log.info('Loaded remote repository URL: %s', remote_repository_url)
    log.info('Loaded local repository path: %s', local_repository)
    log.info('Loaded repository difference outfile path: %s', repository_difference_outfile)
    log.info('Loaded remote repository destination path: %s', remote_repository_destination_path)
    log.info('Loaded log level: %s', log_level)
    log.info('Loaded log file path: %s', log_file_path)

    # Empty values are returned in order to keep Windows and Linux config loader the same
    empty5 = None
    empty6 = None
    return [remote_repository_url, local_repository, repository_difference_outfile,
            remote_repository_destination_path, local_addon_path, empty5, empty6, log_level, log_file_path]
