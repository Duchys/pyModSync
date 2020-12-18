import requests
#TODO: print which file is being downloaded
#Print Addon>filename is being downloaded 
print('Starting the download of @ace3/authors.txt')

url = 'https://a3.417rct.org/addons/%40ace3/authors.txt'\
#TODO: Add configuration option which allows insecure downloads (incase self signed certs are user [or addon repository has expired certificate])
r = requests.get(url)
#TODO: Allow user to specifiy the path
#TODO: Create the @Addon directory (eg.@ace3) (the directory will be granted by the xml with list of addons)
#TODO: Create the Subdiretory in @Addon (eg. @ace3/assets) (the subdirectory name will be granted by the xml with list of addons)
#TODO: Name the file in the same way as specified in the xml list of addons
#TODO: Check if forward slashes work on Windows aswell
#TODO: Optimize the download to not always download the entire file but just the changed parts if possible 
#Write the file to prespecified path by user
with open('/tmp/authors.txt', 'wb') as f:
    f.write(r.content)

# Retrieve HTTP meta-data
#TODO: move this as it is unnecessary here (maybe leave status code for some initial check of the repository, this however will be done in when the repository will be downloaded)
print(r.status_code)
#TODO: delete this
print(r.headers['content-type'])
#TODO: move this as it is unnecessary here (maybe leave status code for some initial check of the repository, this however will be done in when the repository will be downloaded)
print(r.encoding)