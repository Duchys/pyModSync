# Download repository
# Try and except is used to prevent crash incase the remote repository is unavailable
import os
import sys
from file_downloader import file_downloader


def repository_downloader(remote_repository_url, remote_repository_destination_path):
    """The goal of this fuction is to download remote repository
    In case the repository is unavailable, use the cached version instead.
    """

    if remote_repository_url.endswith('/'):
        remote_repository_url = remote_repository_url[:-1]
    print('...........................................')
    print('Updating the remote repository')
    try:
        file_downloader(remote_repository_url, remote_repository_destination_path)
    except ConnectionError:
        if os.path.isfile(remote_repository_destination_path):
            print('Failed to download remote repository, cached repository will be used...')
        else:
            print('...')
            print('Exiting...')
            sys.exit('ERROR: Failed to download remote repository and no cached version found, exiting...')
