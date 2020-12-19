def FileDownloader(file_url,file_destination_path):
    import requests
#TODO: find an alternative which works with GUI aswell
    from clint.textui import progress
#TODO: Add configuration option which allows insecure downloads (incase self signed certs are user [or addon repository has expired certificate])
    file_stream = requests.get(file_url, stream=True)
    print(file_stream.status_code)
#TODO: Set this based on the repository output
#Sets the path to which the file should be put
#TODO: Allow user to specifiy the path
#TODO: Create the @Addon directory (eg.@ace3) (the directory will be granted by the xml with list of addons)
#TODO: Create the Subdiretory in @Addon (eg. @ace3/assets) (the subdirectory name will be granted by the xml with list of addons)
#TODO: Name the file in the same way as specified in the xml list of addons
#TODO: Check if forward slashes work on Windows aswell
#TODO: Optimize the download to not always download the entire file but just the changed parts if possible 
#TODO: Allow pause of the download https://stackoverflow.com/questions/12243997/how-to-pause-and-resume-download-work
#Write the file to prespecified path by user


    with open(file_destination_path, 'wb') as downloaded_file:
        print(f'Starting file download from {file_url}')
        total_length = int(file_stream.headers.get('content-length'))
        for chunk in progress.bar(file_stream.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
            if chunk:
                downloaded_file.write
                downloaded_file.flush
    print(f'File Downloaded from {file_url} was finished')