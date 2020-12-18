#GOAL: The goal of this class is to check if the repository file has changed
#(and possibly store it to compare changes>check with Arcanum, on how the current launcher is handled)
#After the repository is downloaded provide the output of the repository.xml file to FileChangeDetector

#TODO: Call this class on start of the application
#TODO: Call this class on each check request by the user
#TODO: Verify if there is a better way to download files rather than using requests library
import requests
#TODO: print which file is being downloaded
#Print $repo_url is being downloaded
print('Repository xml is being downloaded')

#TODO: Make this configurable by user in the GUI/Configuration
#TODO: Store recent repositories in a config file to easier switching (nice to have)
#TODO: Make sure that the program does not crash when a link to invalid repository is provided
repository_url = 'https://a3.417rct.org/addons/index.xml'\
#TODO: Add configuration option which allows insecure downloads (incase self signed certs are user [or addon repository has expired certificate])
#TODO: Allow pausing the download and resuming the download on later date (tmp folder will probably be required for this, research has to be made)
#TODO: Allow user to specify the bandwith cap for download speed through config file
r = requests.get(url)
#TODO: Allow user to specifiy the path
#TODO: Name the file in the same way as specified in the xml list of addons
#TODO: Check if forward slashes work on Windows aswell
#Write the file to prespecified path by user
with open('/tmp/repository.xml', 'wb') as f:
    f.write(r.content)

# Retrieve HTTP meta-data
#TODO move this as it is unnecessary here (maybe leave status code for some initial check of the repository, this however will be done in when the repository will be downloaded)
print(r.status_code)
#TODO delete this
print(r.headers['content-type'])
#TODO move this as it is unnecessary here (maybe leave status code for some initial check of the repository, this however will be done in when the repository will be downloaded)
print(r.encoding)