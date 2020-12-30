import os
import sys
from file_downloader import file_downloader
from check_for_update import compare_repositories
from check_for_update import check_for_update
from user_checksum_generator import local_repository_generator
from file_update_requester import file_update_requester
from config_manager import create_config
from config_manager import check_if_config_exists
from config_manager import config_loader

# Define variables

# Create initial config which will be then read from
if not check_if_config_exists():
    print('Config file not found, generating new config file...')
    local_addon_path = input('Please enter path to your local addon directory (ie. /opt/Arma3addons): ')
    if local_addon_path.endswith('/'):
        local_addon_path = local_addon_path[:-1]
    remote_repository_url = input('Please enter URL of the remote repository (ie. https://franta.com/remoterepo.csv): ')
    create_config(local_addon_path, remote_repository_url)

print('loading the config...')
config = config_loader()
remote_repository_url = config[0]
local_repository = config[1]
repository_difference_outfile = config[2]
remote_repository_destination_path = config[3]
local_addon_path = config[4]


if remote_repository_url.endswith('/'):
    remote_repository_url = remote_repository_url[:-1]
print('...........................................')
print('Updating the remote repository')
# Download repository
# Try and except is used to prevent crash incase the remote repository is unavailable
try:
    file_downloader(remote_repository_url, remote_repository_destination_path)
except ConnectionError:
    if os.path.isfile(remote_repository_destination_path):
        print('Failed to download remote repository, cached repository will be used...')
    else:
        print('...')
        print('Exiting...')
        sys.exit('ERROR: Failed to download remote repository and no cached version found, exiting...')


# Compare changed files between local addon repostiory (eg. Franta Cihla's local mod folder [/mnt/addons])
# and remote mod repository (eg. 417RCT Official Repository)

# Delete extra / if present
if local_addon_path.endswith('/'):
    local_addon_path = local_addon_path[:-1]

print('Checking if local repository already exists')
print('...........................................')
# Checks if file local repository already exists, if not it calls the generator to generate the local repository
if not os.path.isfile(local_repository):
    print('local repository was not found, generating local repository')
    local_repository_generator(local_addon_path, local_repository)
# Checks if the local repository file is empty, if so, regenerates the local repository
# This is done in order to prevent redownload of already downloaded files
# incase some issue arose during the generation of the initial local repository
elif os.stat(local_repository).st_size == 0:
    print('File exists and is empty, regenerating local repository')
    local_repository_generator(local_addon_path, local_repository)
else:
    print('File exists and is not empty')
print('...........................................')


print('Checking for differences between local and remote repository')
print('...........................................')
# Compare repositories for any differences, and write them to an outfile
compare_repositories(local_repository, remote_repository_destination_path, repository_difference_outfile)
# Check if outfile for repository difference contains any data
while check_for_update(local_repository, remote_repository_destination_path, repository_difference_outfile):
    file_update_requester(remote_repository_url, repository_difference_outfile, local_addon_path, local_repository)
    compare_repositories(local_repository, remote_repository_destination_path, repository_difference_outfile)
print('All files are now synchronized with the remote repository...')
print('Exiting...')
