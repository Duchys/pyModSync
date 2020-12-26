from RepositoryLoader import repository_downloader
from CheckForUpdate import compare_repositories
from CheckForUpdate import check_for_update
from UserChecksumGenerator import local_repository_generator
import os
#TODO: Allow user to specifiy the path
#TODO: Check if forward slashes work on Windows aswell @Furi
#remote_repository_url = 'https://a3.417rct.org/addons/pymodsyncrepo.csv'
remote_repository_destination_path = '/home/duchys/Documents/remoterepository.csv'
#Download repository
#repository_downloader(remote_repository_url, remote_repository_destination_path)

#Compare changed files between local addon repostiory (eg. Franta Cihla's local mod folder [/mnt/addons]) and remote addon repository (eg. 417RCT Official Repository)
local_repository= '/home/duchys/Documents/localrepo.csv'
local_addon_path= '/mnt/ssd/417addons'
repository_difference_outfile= '/home/duchys/Documents/repodiffoutfile.csv'

if not os.path.isfile(local_repository):
    print('local repository was not found, generating local repository')
    local_repository_generator(local_addon_path, local_repository)
elif os.stat(local_repository).st_size == 0:
    print('file exists and is null, regenerating local repository')
    local_repository_generator(local_addon_path, local_repository)
else:
    print('file exists and is not null')


compare_repositories(local_repository, remote_repository_destination_path, repository_difference_outfile)
check_for_update(local_repository, remote_repository_destination_path, repository_difference_outfile)