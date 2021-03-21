import configparser
import os
import logging
import sys
import traceback
from logging.handlers import RotatingFileHandler
import requests

# TODO: Replace steam path \\ to /

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
    LOG_FILE_PATH = 'C:/ProgramData/pyModSync/pymodsync.log'
# If not, hope for linux system
else:
    # Set log path by expanding user home path from ~
    USER_HOME = os.path.expanduser("~")
    LOG_FILE_PATH = USER_HOME + '/.cache/pyModSync/pymodsync.log'
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


def create_config(local_addon_path, remote_repository_url):
    """Generates config file on the initial start of the application
    """
    log = logging.getLogger('pymodsync_logger')
    config = configparser.ConfigParser(allow_no_value=True)
    # If the OS is windows
    log.debug('Checking system type.')
    if os.name == 'nt':
        log.debug('Windows system detected.')
        log.info('Creating configuration for Windows Systems')
        log.info('Reading registry for steam path')

        arma_exe_path = ''
        steam_exe_path = ''
        try:
            # Winreg is imported in here instead of top level, as it would otherwise crash the program on Linux Systems
            import winreg  # pylint: disable=import-error,import-outside-toplevel
            # Registry keys for steam install location
            steam_reg_location_32bit = "SOFTWARE\\Valve\\Steam"
            steam_reg_location_64bit = "SOFTWARE\\WOW6432Node\\Valve\\Steam"
            try:
                log.info('Opening 64-bit Steam registry key')
                print('Opening 64-bit Steam registry key')
                # Open 64-bit steam registry key
                steam_reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, steam_reg_location_64bit)
                # Read values from InstallPath
                steam_exe_path = winreg.QueryValueEx(steam_reg_key, "InstallPath")
                # Add steam.exe to the install path fo steam
                steam_exe_path = str(steam_exe_path[0]) + "\\steam.exe"
                # Toss a exception if path is not found
                log.info('Checking if steam.exe path value from registry is valid')
                if os.path.isfile(steam_exe_path):
                    log.info('Steam path from registry is valid')
                else:
                    log.warning('Steam path from registry is invalid')
                    raise FileNotFoundError(f'{steam_exe_path} not found')
            except (OSError, FileNotFoundError, EnvironmentError) as err:
                log.debug(err)
                print('No 64bit Steam registry key found.')
                log.info('No 64bit Steam registry key found.')
                try:
                    log.info('Opening 32-bit Steam registy key')
                    print("Opening 32-bit Steam registy key")
                    # Open 32-bit steam registry key
                    steam_reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, steam_reg_location_32bit)
                    # Read values from InstallPath
                    steam_exe_path = winreg.QueryValueEx(steam_reg_key, "InstallPath")
                    # Add steam.exe to the install path fo steam
                    steam_exe_path = str(steam_exe_path[0]) + "\\steam.exe"
                    # Toss a exception if path is not found
                    log.info('Checking if steam.exe path value from registry is valid')
                    if os.path.isfile(steam_exe_path):
                        log.info('Steam path from registry is valid')
                    else:
                        log.warning('Steam path from registry is invalid')
                        raise FileNotFoundError(f'{steam_exe_path} not found')
                except (OSError, FileNotFoundError, EnvironmentError) as err:
                    log.debug(err)
                    print('Path to steam not found in registry')
                    log.info('Path to steam not found in registry')
                    log.info('Asking user if steam is installed')
                    # Ask user if steam is installed and transform it to lowercase
                    steam_installed = input('Is steam installed? [YES/no]') or 'yes'
                    steam_installed = steam_installed.lower()
                    # Check if users response is valid
                    while steam_installed not in ('yes', 'y', 'no', 'n'):
                        # if not, ask again
                        log.warning('Invalid entry provided, asking the user if steam is installed again')
                        print('Invalid entry, valid entries are YES, NO, N, Y')
                        steam_installed = input('Is steam installed? [YES/no]') or 'yes'
                        steam_installed = steam_installed.lower()
                    log.debug('User responded %s', steam_installed)
                    if steam_installed in ('yes', 'y'):
                        # If user responded that steam is installed, ask him for path to steam
                        log.info('Asking user for path to steam.exe')
                        steam_exe_path = input('Please enter path to the steam.exe (ie. C:\\Steam\\steam.exe)')
                        # Check if provided path ends in file and if steam is installed
                        while not os.path.isfile(steam_exe_path) and steam_installed in ('yes', 'y'):
                            log.warning('Invalid entry provided, asking the user for path to steam.exe again')
                            print('Invalid path provided, please provide correct path.')
                            # Ask user if steam is really installed
                            steam_installed = input('Is steam really installed? [YES/no]') or 'yes'
                            steam_installed = steam_installed.lower()
                            # Check validity of answer
                            while steam_installed not in ('yes', 'y', 'no', 'n'):
                                # if not, ask again
                                log.warning('Invalid entry provided, asking the user if steam is installed again')
                                print('Invalid entry, valid entries are YES, NO, N, Y')
                                steam_installed = input('Is steam really installed? [YES/no]') or 'yes'
                                steam_installed = steam_installed.lower()
                            if steam_installed in ('yes', 'y'):
                                # Ask user for path to steam.exe
                                steam_exe_path = input('Please enter path to the steam.exe (ie. C:\\Steam\\steam.exe)')
                                log.info('User responded %s', steam_exe_path)
                    else:
                        log.info('Asking the user for path to arma3.exe')
                        # Ask user for path to arma3.exe
                        arma_exe_path = input('Please enter path to your arma3.exe (ie. C:\\Arma3\\arma3.exe)')
                        log.info('User responded %s', arma_exe_path)
                        steam_exe_path = ''
                        while arma_exe_path == '':
                            log.warning('No entry provided, asking the user for path to arma3.exe again')
                            print('No path provided, please provide a path.')
                            arma_exe_path = input('Please enter path to your arma3.exe (ie. C:\\Arma3\\arma3.exe)')
                        while not os.path.isfile(arma_exe_path):
                            log.warning('Invalid entry provided, asking the user for path to arma3.exe again')
                            print('Invalid path provided, please provide correct path.')
                            arma_exe_path = input('Please enter path to the arma3.exe (ie. C:\\Arma3\\arma3.exe)')
                            log.info('User responded %s', arma_exe_path)
                            log.info('Arma3 path is a file')
        # Raise exception if all else fails
        except Exception:
            print('Unhandled exception located.')
            print('Exiting...')
            trace_back = traceback.format_exc()
            log.error(trace_back)
            print(trace_back)

        local_addon_path = local_addon_path.replace('\\', '/')
        remote_repository_destination_path = 'C:/ProgramData/pyModSync/remoterepository.csv'
        local_repository = 'C:/ProgramData/pyModSync/localrepo.csv'
        repository_difference_outfile = 'C:/ProgramData/pyModSync/repodiffoutfile.csv'
        steam_exe_path = steam_exe_path.replace('\\', '/')
        arma_exe_path = arma_exe_path.replace('\\', '/')

        log.info('Setting remote repostiory path to %s', remote_repository_destination_path)
        log.info('Setting local repostiory path to %s', local_repository)
        log.info('Setting repository difference path to %s', repository_difference_outfile)
        log.info('Setting remote repository url to %s', remote_repository_url)
        log.info('Setting local addon path to %s', local_addon_path)
        log.info('Setting Arma3.exe path to %s', arma_exe_path)
        log.info('Setting Steam.exe path to %s', steam_exe_path)
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
        config['GENERAL']['# Path to steam.exe file, if empty, Arma3 is launched through Arma3 executable'] = None
        config['GENERAL']['steam_exe_path'] = steam_exe_path
        config['GENERAL']['# Path to arma3.exe file, if empty, Arma3 is launched through Steam'] = None
        config['GENERAL']['arma_exe_path'] = arma_exe_path
        config['LOGGING'] = {}
        config['LOGGING']['# Log file destination path'] = None
        config['LOGGING']['log_file_path'] = LOG_FILE_PATH
        config['LOGGING']['Set logging level (Options: INFO, WARN, ERROR, DEBUG'] = None
        config['LOGGING']['log_level'] = LOG_LEVEL

        log.info('Checking if C:/ProgramData/pyModSync directory exists')
        # Check if directory for program files exists
        if not os.path.exists('C:/ProgramData/pyModSync'):
            log.info('C:/ProgramData/pyModSync does not exist, creating directories')
            os.makedirs('C:/ProgramData/pyModSync')
        # Write config to file
        with open('C:/ProgramData/pyModSync/pymodsync.properties', 'w') as configfile:
            config.write(configfile)
        log.info('Config created')
        print('Config created')
    # Or if it is other OS, hopefully one that uses the .config and .cache directories :)
    else:
        log.debug('Linux system detected.')
        log.info('Creating configuration for Linux Systems')
        log.info('Reading registry for steam path')

        remote_repository_destination_path = USER_HOME + '/.cache/pyModSync/remoterepository.csv'
        local_repository = USER_HOME + '/.cache/pyModSync/localrepository.csv'
        repository_difference_outfile = USER_HOME + '/.cache/pyModSync/repositorydifference.csv'

        log.info('Setting remote repostiory path to %s', remote_repository_destination_path)
        log.info('Setting local repostiory path to %s', local_repository)
        log.info('Setting repository difference path to %s', repository_difference_outfile)
        log.info('Setting remote repository url to %s', remote_repository_url)
        log.info('Setting local addon path to %s', local_addon_path)
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
        config['GENERAL']['# Location where the file with local checksum repository should be stored'] = None
        config['GENERAL']['local_repository'] = local_repository
        config['GENERAL']['# This file is used only for update purposes'] = None
        config['GENERAL']['repository_difference_outfile'] = repository_difference_outfile
        config['LOGGING'] = {}
        config['LOGGING']['# Log file destination path'] = None
        config['LOGGING']['log_file_path'] = LOG_FILE_PATH
        config['LOGGING']['Set logging level (Options: INFO, WARN, ERROR, DEBUG'] = None
        config['LOGGING']['log_level'] = LOG_LEVEL

        log.info('Checking if %s exists', USER_HOME + '/.config/pyModSync')
        # Creates directories if they do not exist yet
        if not os.path.exists(USER_HOME + '/.config/pyModSync'):
            log.info('%s does not exist, creating directories', USER_HOME + '/.config/pyModSync')
            os.makedirs(USER_HOME + '/.config/pyModSync')
        # Creates directories if they do not exist yet
        log.info('Checking if %s exists', USER_HOME + '/.cache/pyModSync')
        if not os.path.exists(USER_HOME + '/.cache/pyModSync'):
            log.info('%s does not exist, creating directories', USER_HOME + '/.cache/pyModSync')
            os.makedirs(USER_HOME + '/.cache/pyModSync')
        with open(USER_HOME + '/.config/pyModSync/pymodsync.properties', 'w') as configfile:
            config.write(configfile)
        log.info('Config created')
        print('Config created')


def check_if_config_exists():
    """Checks if the configration file is already created
    """
    log = logging.getLogger('pymodsync_logger')
    log.debug('Checking system type')
    # Check system type
    if os.name == 'nt':
        log.info('Windows system detected')

        config_location = 'C:/ProgramData/pyModSync/pymodsync.properties'
        log.info('checking if configuration file exists')
        # Check if config file exists
        if os.path.isfile(config_location):
            log.info('Config file found')
            print('Configuration file found, loading configuration...')
            return 1
        log.info('No config file found')
        print('No configuration file found...')
        log.info('Asking user for path to local addon directory')
        print('Do not use the arma !WORKSHOP directory')
        print('If path does not exist, it will be created')
        # Ask user for local addon directory path
        local_addon_path = input('Please enter path to your local addon directory (ie. C:\\417addons): ')
        log.info('User submitted %s', local_addon_path)
        # Check if path was provided
        while local_addon_path == '':
            print('No addon path provided')
            log.warning('No addon path was provided, asking user again')
            local_addon_path = input('Please enter path to your local addon directory (ie. C:\\417addons): ')
            log.info('User submitted %s', local_addon_path)
        # Check if path is file
        while os.path.isfile(local_addon_path):
            log.warning('Path exists but point to file, asking user again')
            print('Path exists but points to file, please enter valid path')
            local_addon_path = input('Please enter path to your local addon directory (ie. C:\\417addons): ')
            log.info('User submitted %s', local_addon_path)
        # Check if path exists
        if not os.path.isdir(local_addon_path) and not os.path.isfile(local_addon_path):
            print('Directory not found, creating the path.')
            log.info('Valid path provided, creating path')
            # Try to create the path
            try:
                os.makedirs(local_addon_path)
                print(f'{local_addon_path} created')
                log.info('%s path created', local_addon_path)
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
        # Asking user for URL to remote repository
        log.info('Asking user for URL of remote repository')
        remote_repository_url = input('Please enter URL of the remote repository (ie. https://franta.com/repo.csv): ')
        log.info('%s provided as URL of remote repository', remote_repository_url)
        # Check anything was provided
        while remote_repository_url == '':
            print('No url was provided, please provide a URL')
            log.info('No URL was provided')
            remote_repository_url = input('Please enter URL of the remote repository (ie. https://franta.com/repo.csv): ')  # noqa: E501 pylint: disable=line-too-long
            log.info('%s provided as URL of remote repository', remote_repository_url)
            # Check status code of the remote repository
        try:
            log.info('Checking if the remote URL is reachable')
            repo_status = False
            while repo_status is False:
                try:
                    repo_check_status_code = requests.head(remote_repository_url).status_code
                except (requests.exceptions.ConnectionError, requests.exceptions.RequestException):
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
                    remote_repository_url = input('Please enter URL of the remote repository (ie. https://franta.com/repo.csv): ')  # noqa: E501 pylint: disable=line-too-long
                    # Checking if URL is not empty
                    while remote_repository_url == '':
                        print('No URL was provided, please provide a URL')
                        log.info('No URL was provided')
                        # Asking user for new URL
                        remote_repository_url = input('Please enter URL of the remote repository (ie. https://franta.com/repo.csv): ')  # noqa: E501 pylint: disable=line-too-long
                        log.info('%s provided as URL of remote repository', remote_repository_url)
                else:
                    log.info('%s returned status code 200, continuing')
                    repo_status = True
        except (requests.exceptions.ConnectionError, requests.exceptions.RequestException) as err:
            print(f"URL {remote_repository_url} not reachable")
            log.error(err)
            sys.exit()
        # Calling create config fuction
        log.debug('Calling create_config fuction.')
        create_config(local_addon_path, remote_repository_url)
        return 0

    # Linux
    config_location = USER_HOME + '/.config/pyModSync/pymodsync.properties'
    log.info('checking if configuration file exists')
    if os.path.isfile(config_location):
        log.info('Config file found')
        print('Configuration file found, loading configuration...')
        return 1
    log.info('No config file found')
    print('No configuration file found...')
    log.info('Asking user for path to local addon directory')
    print('Do not use the arma !WORKSHOP directory')
    print('If path does not exist, it will be created')
    # Ask user for local addon directory path
    local_addon_path = input('Please enter path to your local addon directory (ie. /opt/Arma3addons): ')
    log.info('User submitted %s', local_addon_path)
    # Check if path was provided
    while local_addon_path == '':
        print('No addon path provided')
        log.warning('No addon path was provided, asking user again')
        local_addon_path = input('Please enter path to your local addon directory (ie. /opt/Arma3addons): ')
        log.info('User submitted %s', local_addon_path)
        # Check if path is file
    while os.path.isfile(local_addon_path):
        log.warning('Path exists but point to file, asking user again')
        print('Path exists but points to file, please enter valid path')
        local_addon_path = input('Please enter path to your local addon directory (ie. /opt/Arma3addons): ')
        log.info('User submitted %s', local_addon_path)
    # Check if path exists
    if not os.path.isdir(local_addon_path) and not os.path.isfile(local_addon_path):
        print('Directory not found, creating the path.')
        log.info('Valid path provided, creating path')
        # Try to create the path
        try:
            os.makedirs(local_addon_path)
            print(f'{local_addon_path} created')
            log.info('%s path created', local_addon_path)
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
        log.info('Removing leading slash from path')
        # Remove leading / from the path if present
        log.debug('Checking if leading slash is present')
        if local_addon_path.endswith('/'):
            local_addon_path = local_addon_path[:-1]
            log.debug('Leading slash removed from path')
    log.info('Asking user for URL of remote repository')
    remote_repository_url = input('Please enter URL of the remote repository (ie. https://franta.com/repo.csv): ')
    log.info('%s provided as URL of remote repository', remote_repository_url)
    # Check anything was provided
    while remote_repository_url == '':
        print('No url was provided, please provide a URL')
        log.info('No URL was provided')
        remote_repository_url = input('Please enter URL of the remote repository (ie. https://franta.com/repo.csv): ')  # noqa: E501 pylint: disable=line-too-long
        log.info('%s provided as URL of remote repository', remote_repository_url)

    # Check status code of the remote repository
    try:
        log.info('Checking if the remote URL is reachable')
        repo_status = False
        while repo_status is False:
            try:
                repo_check_status_code = requests.head(remote_repository_url).status_code
            except (requests.exceptions.ConnectionError, requests.exceptions.RequestException):
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
                remote_repository_url = input('Please enter URL of the remote repository (ie. https://franta.com/repo.csv): ')  # noqa: E501 pylint: disable=line-too-long
                # Checking if URL is not empty
                while remote_repository_url == '':
                    print('No URL was provided, please provide a URL')
                    log.info('No URL was provided')
                    # Asking user for new URL
                    remote_repository_url = input('Please enter URL of the remote repository (ie. https://franta.com/repo.csv): ')  # noqa: E501 pylint: disable=line-too-long
                    log.info('%s provided as URL of remote repository', remote_repository_url)
            else:
                log.info('%s returned status code 200, continuing')
                repo_status = True
    except (requests.exceptions.ConnectionError, requests.exceptions.RequestException) as err:
        print(f"URL {remote_repository_url} not reachable")
        log.error(err)
        sys.exit()
        # Calling create config fuction
        log.debug('Calling create_config fuction.')
    create_config(local_addon_path, remote_repository_url)
    return 0


def config_loader():
    """Loads the configuration file and returns the values as variables
    """
    log = logging.getLogger('pymodsync_logger')
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
    log.info('Loaded steam.exe path: %s', steam_exe_path)
    log.info('Loaded arma3.exe path: %s', arma_exe_path)
    log.info('Loaded log level: %s', log_level)
    log.info('Loaded log file path: %s', log_file_path)

    return [remote_repository_url, local_repository, repository_difference_outfile,
            remote_repository_destination_path, local_addon_path, log_level, log_file_path]
