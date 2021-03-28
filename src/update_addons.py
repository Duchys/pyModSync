from update_manager import check_for_update
from update_manager import file_update_requester
from update_manager import compare_repositories
from config_manager import config_loader
from config_manager import check_if_config_exists
from logger import logger


def update_addons():
    """Update out of date addons
    """
    log = logger()
    # Load config
    check_if_config_exists()
    config = config_loader()
    remote_repository_url = config[0]
    local_repository = config[1]
    repository_difference_outfile = config[2]
    remote_repository_destination_path = config[3]
    local_addon_path = config[4]

    # Download new addons and updates local repository
    # Check for if there is still some update present
    while check_for_update(local_repository, remote_repository_destination_path, repository_difference_outfile):
        file_update_requester(remote_repository_url, repository_difference_outfile, local_addon_path, local_repository)
        compare_repositories(local_repository, remote_repository_destination_path, repository_difference_outfile)

    log.info('All files are now synchronized with the remote repository')
    print('All files are now synchronized with the remote repository...')
    print('Exiting...')
