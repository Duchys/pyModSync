# Download repository
# Try and except is used to prevent crash incase the remote repository is unavailable
import os
import sys
from file_downloader import file_downloader
from logger import logger


def repository_downloader(remote_repository_url, remote_repository_destination_path):
    """The goal of this fuction is to download remote repository
    In case the repository is unavailable, use the cached version instead.
    """
    log = logger()
    if remote_repository_url.endswith('/'):
        remote_repository_url = remote_repository_url[:-1]
    print('...........................................')
    log.info('Updating the remote repository')
    print('Updating the remote repository')
    try:
        file_downloader(remote_repository_url, remote_repository_destination_path)
    except ConnectionError:
        log.warning('Failed to download remote repository, checking if cached repository exists')
        if os.path.isfile(remote_repository_destination_path):
            log.warning('Cached repository found, loading cached repository...')
            print('Failed to download remote repository, cached repository will be used...')
        else:
            print('...')
            print('Exiting...')
            log.error('Failed to download remote repository, and no cached repository found')
            log.error('Exiting...')
            sys.exit('ERROR: Failed to download remote repository and no cached version found, exiting...')
