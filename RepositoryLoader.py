#GOAL: The goal of this function is to check if the repository file has changed
#(and possibly store it to compare changes>check with Arcanum, on how the current launcher is handled)
#After the repository is downloaded provide the output of the repository.xml file to FileChangeDetector
from FileDownloader import FileDownloader
#TODO: Call this function on start of the application
#TODO: Call this function on each check request by the user
#TODO: find an alternative which works with GUI aswell
#TODO: print which file is being downloaded
#Print $repo_url is being downloaded
#TODO: Make this configurable by user in the GUI/Configuration
#TODO: Store recent repositories in a config file to easier switching (nice to have)
#TODO: Make sure that the program does not crash when a link to invalid repository is provided
repository_url = 'https://a3.417rct.org/addons/index.xml'
repository_destination_path = '/tmp/repo.xml'
#TODO: Allow user to specifiy the path
#TODO: Check if forward slashes work on Windows aswell @Furi
#Write the file to prespecified path by user
FileDownloader(repository_url, repository_destination_path)