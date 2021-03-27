import os
import sys
import errno
import requests
from tqdm import tqdm
from logger import logger


def file_downloader(file_url, file_destination_path):
    """When this fuction is called, file_url is downloaded and stored in file_destination_path
    """
    log = logger()
    file_stream = requests.get(file_url, stream=True, timeout=60)
    # Sets the path to which the file should be put
    # Write the file to prespecified path by user

    print('...........................................')
    # Check if file is available
    log.info('Checking if the remote URL is reachable')
    file_status = False
    retry_count = 0
    while (retry_count < 3 and file_status is False):
        try:
            url_check_status_code = requests.head(file_url, timeout=15).status_code
            log.info('Received %s status code', url_check_status_code)
        except (requests.exceptions.ConnectionError,
                requests.exceptions.RequestException,
                requests.exceptions.Timeout):
            # Set to status code if site is not reachable 451
            url_check_status_code = 451
            log.info('%s was not reachable, setting status code to 451', file_url)

        if url_check_status_code == 200:
            # Get the total size of the file
            total_length = int(file_stream.headers.get('content-length', 0))
            print(f'URL {file_url} returned status code 200, starting download')
            log.info('%s returned status code 200, starting download', file_url)
            # create file download file in path file_destination_path and prepare to wirte to it
            # also sets up tqdm download progress bar
            filename = file_url.split('/')[-1]
            # Create directory path if it does not exist
            log.info('Checking if addon sub-directories already exist')
            if not os.path.exists(os.path.dirname(file_destination_path)):
                try:
                    log.info('Addon sub-directory not found, creating directory')
                    os.makedirs(os.path.dirname(file_destination_path))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            with open(file_destination_path, 'wb') as downloaded_file, tqdm(
                # TQDM progress bar configuration
                desc=filename,
                total=total_length,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
                # More TQDM progress bar stuff
            ) as download_bar:
                # Sets the size of each chunk in the download bar
                for data in file_stream.iter_content(chunk_size=1024):
                    # Save the file in file_destination_path
                    size = downloaded_file.write(data)
                    # Update download bar based on downloaded size
                    download_bar.update(size)
            log.info('%s downloaded succesfully from URL %s', filename, file_url)
            print(f'{filename} was sucessfully downloaded from URL {file_url}')
            file_status = True

        # If page is not found
        elif url_check_status_code == 404:
            log.warning('Download failed, current retry count is %s', retry_count)
            retry_count += 1
        # If not 200 and 404 code is found
        else:
            log.warning('Download failed, current retry count is %s', retry_count)
            retry_count += 1
    if file_status is False:
        log.error('Retry amount for %s reached', file_url)
        sys.exit('Retry amount reached, file not downloaded, exiting...')
