def file_downloader(file_url, file_destination_path):
    import requests
    import sys
    import errno
    import os
    from tqdm import tqdm
    file_stream = requests.get(file_url, stream=True)
#    print(file_stream.status_code)
#Sets the path to which the file should be put
#Write the file to prespecified path by user

    print('...........................................')
    #Check if file is available
    if file_stream.status_code == 200:
        #Get the total size of the file
        total_length = int(file_stream.headers.get('content-length', 0))
        print(f'URL {file_url} returned status code 200, starting download')
        print('')
        #create file download file in path file_destination_path and prepare to wirte to it
        #also sets up tqdm download progress bar
        filename = file_url.split('/')[-1]
        #Create directory path if it does not exist
        if not os.path.exists(os.path.dirname(file_destination_path)):
            try:
                os.makedirs(os.path.dirname(file_destination_path))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(file_destination_path, 'wb') as downloaded_file, tqdm(
            #TQDM progress bar configuration
            desc=filename,
            total=total_length,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
            #More TQDM progress bar stuff
        ) as download_bar:
            #Sets the size of each chunk in the download bar
            for data in file_stream.iter_content(chunk_size=1024):
                #Save the file in file_destination_path
                size = downloaded_file.write(data)
                #Update download bar based on downloaded size
                download_bar.update(size)
        print('')
        print(f'{filename} was sucessfully downloaded from URL {file_url}')
    #If page is not found, exit
    elif file_stream.status_code == 404:
        sys.exit(f'ERROR: {file_url} not found, status code {file_stream.status_code} returned, exiting...')
    #If not 200 and 404 code is found, exit.
    else:
        sys.exit(f'ERROR: {file_url} returned status code {file_stream.status_code}, exiting...')
    print('...........................................')
    