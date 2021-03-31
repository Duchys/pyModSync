from config_manager import config_loader
from config_manager import create_config_if_not_exist
from repository_downloader import repository_downloader
from local_repository_manager import check_for_local_repository
from update_manager import compare_repositories
from update_manager import check_for_update
from logger import logger


# File intended to be called by GUI
# The goal of this file is to download new repository
# Check for differnces between local and remote repository
# Request download of updated files
# update local repository


def check_addons():
    """Download remote repository
    Compare with local repository
    download changed addons
    Compare changed files between local addon repostiory (eg. Franta Cihla's local mod folder [/mnt/addons])
    and remote mod repository (eg. 417RCT Official Repository)
    """
    # Check if config file exists, if not create it
    create_config_if_not_exist()
    # Define log config by calling logger function
    log = logger()
    log.info('Loading configuration')
    print('Loading configuration')
    # Load configuration
    config = config_loader()
    remote_repository_url = config[0]
    local_repository = config[1]
    repository_difference_outfile = config[2]
    remote_repository_destination_path = config[3]
    local_addon_path = config[4]
    # Download repository
    repository_downloader(remote_repository_url, remote_repository_destination_path)
    # Check for differences
    check_for_local_repository(local_addon_path, local_repository)
    log.info('Checking for differences between local and remote repository')
    print('Checking for differences between local and remote repository')
    print('...........................................')
    # Compare repositories for any differences, and write them to an outfile
    compare_repositories(local_repository, remote_repository_destination_path, repository_difference_outfile)
    # Check if there is difference between local and remote repository
    check_for_update(local_repository, remote_repository_destination_path, repository_difference_outfile)
