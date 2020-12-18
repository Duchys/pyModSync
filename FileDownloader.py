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
#Write the file to prespecified path by user
with open('/tmp/authors.txt', 'wb') as f:
    f.write(r.content)

# Retrieve HTTP meta-data
#TODO delete this shit as it is unnecessary
print(r.status_code)
print(r.headers['content-type'])
print(r.encoding)