import configparser
import os


def create_config(local_addon_path, remote_repository_url):
    """Generates config file on the initial start of the application
    """
    config = configparser.ConfigParser(allow_no_value=True)
    # If the OS is windows
    if os.name == 'nt':
        import winreg
        steam_reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\\WOW6432Node\\Valve\\Steam")
        steam_exe_path = winreg.QueryValueEx(steam_reg_key, "InstallPath")
        print(steam_exe_path)
        print(steam_reg_key)
        print('Using configuration for Windows Systems')
        config['GENERAL'] = {}
        config['GENERAL']['# URL where the remote repository is available'] = None
        config['GENERAL']['remote_repository_url'] = remote_repository_url
        config['GENERAL']['# Location where the file containing the remote checksum repository should be downloaded to'] = None  # noqa: E501 pylint: disable=line-too-long
        config['GENERAL']['remote_repository_destination_path'] = 'C:/ProgramData/pyModSync/remoterepository.csv'
        config['GENERAL']['# Addon folder location'] = None
        config['GENERAL']['local_addon_path'] = local_addon_path
        config['GENERAL']['# Location where the file with local checksum repository should be stored'] = None
        config['GENERAL']['local_repository'] = 'C:/ProgramData/pyModSync/localrepo.csv'
        config['GENERAL']['# This file is used only for update purposes'] = None
        config['GENERAL']['repository_difference_outfile'] = 'C:/ProgramData/pyModSync/repodiffoutfile.csv'
        config['GENERAL']['# Path to steam.exe file'] = None
        config['GENERAL']['steam_exe_path'] = steam_exe_path

        if not os.path.exists('C:/ProgramData/pyModSync'):
            os.makedirs('C:/ProgramData/pyModSync')
        with open('C:/ProgramData/pyModSync/pymodsync.properties', 'w') as configfile:
            config.write(configfile)
        print('Config created')
    # Or if it is other OS, hopefully one that uses the .config and .cache directories :)
    else:
        # Sets the user home directory
        print('Using configuration for Linux')
        user_home = os.path.expanduser("~")
        remote_repository_destination_path = user_home + '/.cache/pyModSync/remoterepository.csv'
        local_repository = user_home + '/.cache/pyModSync/localrepository.csv'
        repository_difference_outfile = user_home + '/.cache/pyModSync/repositorydifference.csv'
        config['GENERAL'] = {}
        config['GENERAL']['# URL where the remote repository is available'] = None
        config['GENERAL']['remote_repository_url'] = remote_repository_url
        config['GENERAL']['# Location where the file containing the remote checksum repository should be downloaded to'] = None  # noqa: E501 pylint: disable=line-too-long
        config['GENERAL']['remote_repository_destination_path'] = remote_repository_destination_path
        config['GENERAL']['# Addon folder location'] = None
        config['GENERAL']['local_addon_path'] = local_addon_path
        config['GENERAL']['# Location where the file with local checksum repository should be stored'] = None
        config['GENERAL']['local_repository'] = local_repository
        config['GENERAL']['# This file is used only for update purposes'] = None
        config['GENERAL']['repository_difference_outfile'] = repository_difference_outfile
        # Creates directories if they do not exist yet
        if not os.path.exists(user_home + '/.config/pyModSync'):
            os.makedirs(user_home + '/.config/pyModSync')
        # Creates directories if they do not exist yet
        if not os.path.exists(user_home + '/.cache/pyModSync'):
            os.makedirs(user_home + '/.cache/pyModSync')

        with open(user_home + '/.config/pyModSync/pymodsync.properties', 'w') as configfile:
            config.write(configfile)
        print('Config created')


def check_if_config_exists():
    """Checks if the configration file is already created
    """
    if os.name == 'nt':
        config_location = 'C:/ProgramData/pyModSync/pymodsync.properties'
        if os.path.isfile(config_location):
            print('Configuration file found, loading configuration...')
            return 1
        print('No configuration file found...')
        local_addon_path = input('Please enter path to your local addon directory (ie. C:\\417addons): ')
        if local_addon_path.endswith('/'):
            local_addon_path = local_addon_path[:-1]
        remote_repository_url = input('Please enter URL of the remote repository (ie. https://franta.com/repo.csv): ')
        create_config(local_addon_path, remote_repository_url)
        return 0
    else:
        user_home = os.path.expanduser("~")
        config_location = user_home + '/.config/pyModSync/pymodsync.properties'
        if os.path.isfile(config_location):
            print('Configuration file found, loading configuration...')
            return 1
        print('Config file not found, generating new config file...')
        local_addon_path = input('Please enter path to your local addon directory (ie. /opt/Arma3addons): ')
        if local_addon_path.endswith('/'):
            local_addon_path = local_addon_path[:-1]
        remote_repository_url = input('Please enter URL of the remote repository (ie. https://franta.com/repo.csv): ')
        create_config(local_addon_path, remote_repository_url)
        return 0


def config_loader():
    """Loads the configuration file and returns the values as variables
    """
    config = configparser.ConfigParser()
    if os.name == 'nt':
        # Path to config file
        config_location = 'C:/ProgramData/pyModSync/pymodsync.properties'
        # Reads the config file
        config.read(config_location)
        print(f'Loading configuration from {config_location}')
        # Saves contents of config file to variables
        remote_repository_url = config['GENERAL']['remote_repository_url']
        local_repository = config['GENERAL']['local_repository']
        repository_difference_outfile = config['GENERAL']['repository_difference_outfile']
        remote_repository_destination_path = config['GENERAL']['remote_repository_destination_path']
        local_addon_path = config['GENERAL']['local_addon_path']
        return [remote_repository_url, local_repository, repository_difference_outfile, remote_repository_destination_path, local_addon_path]  # noqa: E501 pylint: disable=line-too-long
    else:
        print('Linux detected')
        # Sets variable to contain home directory of current user
        user_home = os.path.expanduser("~")
        # Path to config file
        config_location = user_home + '/.config/pyModSync/pymodsync.properties'
        # Reads the config file
        config.read(config_location)
        # Saves contents of config file to variables
        remote_repository_url = config['GENERAL']['remote_repository_url']
        local_repository = config['GENERAL']['local_repository']
        repository_difference_outfile = config['GENERAL']['repository_difference_outfile']
        remote_repository_destination_path = config['GENERAL']['remote_repository_destination_path']
        local_addon_path = config['GENERAL']['local_addon_path']
        return [remote_repository_url, local_repository, repository_difference_outfile, remote_repository_destination_path, local_addon_path]  # noqa: E501 pylint: disable=line-too-long
