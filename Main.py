from RepositoryLoader import repository_downloader
from CheckForUpdate import compare_repositories
from CheckForUpdate import check_for_update
#TODO: Allow user to specifiy the path
#TODO: Check if forward slashes work on Windows aswell @Furi
remote_repository_url = 'https://a3.417rct.org/addons/index.xml'
remote_repository_destination_path = '/home/duchys/Documents/fakeremoterepo.csv'
#Download repository
#repository_downloader(remote_repository_url, remote_repository_destination_path)

#Compare changed files between local addon repostiory (eg. Franta Cihla's local mod folder [/mnt/addons]) and remote addon repository (eg. 417RCT Official Repository)
local_repository= '/home/duchys/Documents/localrepo.csv'
repository_difference_outfile= '/home/duchys/Documents/repodiffoutfile.csv'
compare_repositories(local_repository, remote_repository_destination_path, repository_difference_outfile)
check_for_update(local_repository, remote_repository_destination_path, repository_difference_outfile)