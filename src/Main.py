from FileDownloader import file_downloader
from CheckForUpdate import compare_repositories
from CheckForUpdate import check_for_update
from UserChecksumGenerator import local_repository_generator
from FileUpdateRequester import file_update_requester
import os
#TODO: Allow user to specifiy the path
#TODO: Check if forward slashes work on Windows aswell @Furi
remote_repository_url = 'https://a3.417rct.org/addons/a_debilek_roku_vyhravaz_duchy.csv'
if remote_repository_url.endswith('/'):
    remote_repository_url = remote_repository_url[:-1]
remote_repository_destination_path = '/home/duchys/Documents/remoterepository.csv'
print('...........................................')
print ('Updating the remote repository')
#Download repository
#Try and except is used to prevent crash incase the remote repository is unavailable
try:
    file_downloader(remote_repository_url, remote_repository_destination_path)
except:
    print('failed to download the repository, cached repository will be used...')
#Compare changed files between local addon repostiory (eg. Franta Cihla's local mod folder [/mnt/addons]) and remote addon repository (eg. 417RCT Official Repository)
local_repository= '/home/duchys/Documents/localrepo.csv'

local_addon_path= '/mnt/ssd/417addons'
#Delete extra / if present
if local_addon_path.endswith('/'):
    local_addon_path = local_addon_path[:-1]
repository_difference_outfile= '/home/duchys/Documents/repodiffoutfile.csv'

print('Checking if local repository already exists')
print('...........................................')
#Checks if file local repository already exists, if not it calls the generator to generate the local repository
if not os.path.isfile(local_repository):
    print('local repository was not found, generating local repository')
    local_repository_generator(local_addon_path, local_repository)
#Checks if the local repository file is empty, if so, regenerates the local repository
#this is done in order to prevent redownload of already downloaded files incase some issue arose during the generation of the initial local repository 
elif os.stat(local_repository).st_size == 0:
    print('File exists and is empty, regenerating local repository')
    local_repository_generator(local_addon_path, local_repository)
else:
    print('File exists and is not empty')
print('...........................................')


print('Checking for differences between local and remote repository')
print('...........................................')
#Compare repositories for any differences, and write them to an outfile
compare_repositories(local_repository, remote_repository_destination_path, repository_difference_outfile)
#Check if outfile for repository difference contains any data
while check_for_update(local_repository, remote_repository_destination_path, repository_difference_outfile):
    #tady zavolej něco co ty data vytáhne
    file_update_requester(remote_repository_url,repository_difference_outfile,local_addon_path,local_repository)
    compare_repositories(local_repository, remote_repository_destination_path, repository_difference_outfile)
print('All files are now synchronized with the remote repository...')
print('Exiting...')