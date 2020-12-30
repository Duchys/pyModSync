import configparser
import os
local_addon_path = '/mnt/ssd/417addons'
remote_repository_url = 'https://a3.417rct.org/addons/a_debilek_roku_vyhrava_duchy.csv'
def create_config(local_addon_path,remote_repository_url):
    config = configparser.ConfigParser(allow_no_value=True)
    #If the OS is windows
    if os.name == 'nt':
        print('Using configuration for Windows Systems')
        config['GENERAL'] = {}
        config['GENERAL']['#URL where the remote repository is available'] = None
        config['GENERAL']['remote_repository_url'] = remote_repository_url
        config['GENERAL']['#Location where the file containing the remote checksum repository should be downloaded to'] = None
        config['GENERAL']['remote_repository_destination_path'] = 'C:/ProgramData/pyModSync/remoterepository.csv'
        config['GENERAL']['#Addon folder location'] = None
        config['GENERAL']['local_addon_path']= local_addon_path
        config['GENERAL']['#Location where the file with local checksum repository should be stored'] = None
        config['GENERAL']['local_repository']= 'C:/ProgramData/pyModSync/localrepo.csv'
        config['GENERAL']['#This file is used only for update purposes'] = None
        config['GENERAL']['repository_difference_outfile']= 'C:/ProgramData/pyModSync/repodiffoutfile.csv'

        if not os.path.exists('C:/ProgramData/pyModSync'):
            os.makedirs('C:/ProgramData/pyModSync')
        with open('C:/ProgramData/pyModSync/pymodsync.properties', 'w') as configfile:
            config.write(configfile)
        print('Config created')
#Or if it is other OS, hopefully one that uses the .config and .cache directories :)
    else:
        #Sets the user home directory
        print('Using configuration for Linux')
        user_home = os.path.expanduser("~")
        remote_repository_destination_path = user_home + '/.cache/pyModSync/remoterepository.csv'
        local_repository = user_home + '/.cache/pyModSync/localrepository.csv'
        repository_difference_outfile = user_home + '/.cache/pyModSync/repositorydifference.csv'
        config['GENERAL'] = {}
        config['GENERAL']['#URL where the remote repository is available'] = None
        config['GENERAL']['remote_repository_url'] = remote_repository_url
        config['GENERAL']['#Location where the file containing the remote checksum repository should be downloaded to'] = None
        config['GENERAL']['remote_repository_destination_path'] = remote_repository_destination_path
        config['GENERAL']['#Addon folder location'] = None
        config['GENERAL']['local_addon_path']= local_addon_path
        config['GENERAL']['#Location where the file with local checksum repository should be stored'] = None
        config['GENERAL']['local_repository']= local_repository
        config['GENERAL']['#This file is used only for update purposes'] = None
        config['GENERAL']['repository_difference_outfile']= repository_difference_outfile
        #Creates directories if they do not exist yet
        if not os.path.exists(user_home + '/.config/pyModSync'):
            os.makedirs(user_home + '/.config/pyModSync')
        #Creates directories if they do not exist yet
        if not os.path.exists(user_home + '/.cache/pyModSync'):
            os.makedirs(user_home + '/.cache/pyModSync')

        with open(user_home + '/.config/pyModSync/pymodsync.properties', 'w') as configfile:
            config.write(configfile)
        print('Config created')

def check_if_config_exists():
    if os.name == 'nt':
        config_location = 'C:/ProgramData/pyModSync/pymodsync.properties'
        if os.path.isfile(config_location):
            print('Configuration file found, loading configuration...')
            return 1
        else:
            print('No configuration file found...')
            return 0
    else:
        user_home = os.path.expanduser("~")
        config_location = user_home + '/.config/pyModSync/pymodsync.properties'
        if os.path.isfile(config_location):
            print('Configuration file found, loading configuration...')
            return 1
        else:
            print('No configuration file found...')
            return 0




def config_loader():
    config = configparser.ConfigParser()
    if os.name == 'nt':
        
        #Path to config file
        config_location = 'C:/ProgramData/pyModSync/pymodsync.properties'
        #Reads the config file
        config.read(config_location)
        print(f'Loading configuration from {config_location}')
        #Saves contents of config file to variables
        remote_repository_url = config['GENERAL']['remote_repository_url']
        local_repository = config['GENERAL']['local_repository']
        repository_difference_outfile = config['GENERAL']['repository_difference_outfile']
        remote_repository_destination_path = config['GENERAL']['remote_repository_destination_path']
        local_addon_path = config['GENERAL']['local_addon_path']
        return [remote_repository_url,local_repository,repository_difference_outfile,remote_repository_destination_path,local_addon_path]
    else:
        print('Linux detected')
        #Sets variable to contain home directory of current user
        user_home = os.path.expanduser("~")
        #Path to config file
        config_location = user_home + '/.config/pyModSync/pymodsync.properties'
        #Reads the config file
        config.read(config_location)
        #Saves contents of config file to variables
        remote_repository_url = config['GENERAL']['remote_repository_url']
        local_repository = config['GENERAL']['local_repository']
        repository_difference_outfile = config['GENERAL']['repository_difference_outfile']
        remote_repository_destination_path = config['GENERAL']['remote_repository_destination_path']
        local_addon_path = config['GENERAL']['local_addon_path']
        return [remote_repository_url,local_repository,repository_difference_outfile,remote_repository_destination_path,local_addon_path]