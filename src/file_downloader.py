import os
import errno
import requests
from tqdm import tqdm
from logger import logger


def get_status_code(url):
    """Get status code from provided URL
    """
    log = logger()
    try:
        url_status_code = requests.head(url, timeout=15).status_code
        log.info('Received %s status code', url_status_code)
        return url_status_code
    except (requests.exceptions.ConnectionError,
            requests.exceptions.RequestException,
            requests.exceptions.Timeout):
        # Set to status code if site is not reachable 451
        url_status_code = 451
        log.info('%s was not reachable, setting status code to 451', url)
        return url_status_code


def create_addon_path(file_destination_path):
    """Creates the directories in case they are not present for the provided path.
    """
    log = logger()
    # Create directory path if it does not exist
    log.info('Checking if addon sub-directories already exist')
    if not os.path.exists(os.path.dirname(file_destination_path)):
        try:
            log.info('Addon sub-directory not found, creating directory')
            os.makedirs(os.path.dirname(file_destination_path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def file_downloader(file_url, file_destination_path):
    """When this fuction is called, file_url is downloaded and stored in file_destination_path
    """
    log = logger()
    try:
        file_stream = requests.get(file_url, stream=True, timeout=60)
    except (requests.exceptions.ConnectionError,
            requests.exceptions.RequestException,
            requests.exceptions.Timeout):
        print('Failed to reach the url: %s', file_url)
    # Sets the path to which the file should be put
    # Write the file to prespecified path by user
    create_addon_path(file_destination_path)
    # Check if file is available
    log.info('Checking if the remote URL is reachable')
    file_status = False
    retry_count = 0
    while (retry_count < 3 and file_status is False):
        url_status_code = get_status_code(file_url)
        if url_status_code == 200:
            # Get the total size of the file
            total_length = int(file_stream.headers.get('content-length', 0))
            # Lock stdout until the print finishes to prevent issues with threading
            log.info('%s returned status code 200, starting download', file_url)
            # create file download file in path file_destination_path and prepare to wirte to it
            # also sets up tqdm download progress bar
            filename = file_url.split('/')[-1]
            # Open destination path of the file for writing
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
            downloaded_file.close()
            download_bar.close()
            log.info('%s downloaded succesfully from URL %s', filename, file_url)
            file_status = True
        # If page is not found
        elif url_status_code == 404:
            log.warning('Download failed, current retry count is %s', retry_count)
            retry_count += 1
        # If not 200 and 404 code is found
        else:
            log.warning('Download failed, current retry count is %s', retry_count)
            retry_count += 1
    # If retry count was reached and the file was not downloaded
    # Exit the application with error
    if file_status is False:
        log.error('Retry amount for %s reached', file_url)
        raise ConnectionError('Retry amount reached, file not downloaded, exiting...')
