from config_manager import config_loader
from config_manager import check_if_config_exists
from repository_downloader import repository_downloader
from local_repository_manager import check_for_local_repository
from update_manager import compare_repositories
from update_manager import check_for_update


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
    check_if_config_exists()
    print('loading the config...')
    config = config_loader()
    remote_repository_url = config[0]
    local_repository = config[1]
    repository_difference_outfile = config[2]
    remote_repository_destination_path = config[3]
    local_addon_path = config[4]

    repository_downloader(remote_repository_url, remote_repository_destination_path)
    check_for_local_repository(local_addon_path, local_repository)

    print('Checking for differences between local and remote repository')
    print('...........................................')
    # Compare repositories for any differences, and write them to an outfile
    compare_repositories(local_repository, remote_repository_destination_path, repository_difference_outfile)
    # Check if there is difference between local and remote repository
    check_for_update(local_repository, remote_repository_destination_path, repository_difference_outfile)
