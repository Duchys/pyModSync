#GOAL: The goal of this function is to check if the repository file has changed
#(and possibly store it to compare changes>check with Arcanum, on how the current launcher is handled)
#After the repository is downloaded provide the output of the repository.xml file to FileChangeDetector
from FileDownloader import file_downloader
#TODO: Call this function on start of the application
#TODO: Call this function on each check request by the user
#TODO: find an alternative which works with GUI aswell
#TODO: print which file is being downloaded
#Print $repo_url is being downloaded
#TODO: Make this configurable by user in the GUI/Configuration
#TODO: Store recent repositories in a config file to easier switching (nice to have)
#TODO: Make sure that the program does not crash when a link to invalid repository is provided
#TENHLE FILE JE VLASTNĚ ÚPLNĚ K HOVNU
remote_repository_url = ''
remote_repository_destination_path = ''
def repository_downloader(remote_repository_url, remote_repostiory_destination_path):
    file_downloader(remote_repository_url, remote_repostiory_destination_path)

#Start download of the repository and store it in the repository_destination_path


#TODO: Check if the has changed from the previous time the repository was downloaded (nice to have)