import os
import csv
import hashlib
from local_repository_manager import file_hash_hex
from file_downloader import file_downloader
from logger import logger


def compare_repositories(local_repository, remote_repository_destination_path, repository_difference_outfile):
    """Compare local and remote repositori
    """
    log = logger()
    log.info('Comparing repositories')
    # Opens repo csv files
    log.debug('Opening local repository in path: %s', local_repository)
    with open(local_repository, 'r', encoding="utf8") as local_repo:
        local_repo = local_repo.readlines()
    log.debug('Opening remote repository in path: %s', remote_repository_destination_path)
    with open(remote_repository_destination_path, 'r', encoding="utf8") as remote_repo:
        # Skips first 2 lines
        remote_repo = remote_repo.readlines()[2:]
    # Compares local repository with remote repostitory
    log.debug('Creating repository difference outfile i npath: %s', repository_difference_outfile)
    with open(repository_difference_outfile, 'w', encoding="utf8") as repo_diff:
        # Each line present in remote repostiory gets compared to the local_repository.
        # If the line is not present (ie. not exact match) it gets put to a repo_diff .csv file.
        for line in remote_repo:
            if line not in local_repo:
                log.debug('%s line not found, adding to outfile', line)
                repo_diff.write(line)


def check_for_update(local_repository, remote_repository_destination_path, repository_difference_outfile):
    """Checks if there is any difference between repositories based on output of compare_repositories
    """
    log = logger()
    # Call compare_repositories fuction to create repository difference outfile
    compare_repositories(local_repository, remote_repository_destination_path, repository_difference_outfile)
    log.info('Checking if update occured')
    # Check if update occured
    if not os.stat(repository_difference_outfile).st_size == 0:
        log.info('Update detected')
        print('Change between local and remote repository was detected')
        return 1
    log.info('No update detected')
    print('No change between local and remote repository was detected')
    print('...........................................')
    return 0


def update_checksum(updated_file, local_repository, updated_file_path):
    """Update checksum of the updated file in the local repository
    """
    # Read local repository to memory
    log = logger()
    log.debug('Reading %s to memory', local_repository)
    with open(local_repository, encoding="utf8") as inlocalrepo:
        reader = csv.reader(inlocalrepo.readlines(), delimiter='\t')

    local_repository_temp_destination = local_repository+'_temp'
    log.debug('Creating temporary file %s', local_repository_temp_destination)
    # Create temporary file without the line containing the hash of the updated file
    with open(local_repository_temp_destination, 'w', newline='', encoding='utf-8') as outlocalrepo:
        writer = csv.writer(outlocalrepo, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        log.info('Updating checksum of %s', updated_file)
        print(f'Updating checksum of {updated_file}')
        for line in reader:
            # If the line does not contain the filaneme of the updated file it will be rewriten to the updated repo
            if not updated_file == line[0]:
                writer.writerow(line)
            else:
                log.debug('Line containing %s found in the local repository, removing the line', updated_file)
                print(f'Line containing {updated_file} found in the local repository, removing the line...')
        # Generate hash for the updated file on the end of the line
        writer.writerow((updated_file, file_hash_hex(updated_file_path, hashlib.blake2b)))
    # Move the temporary repository to the local_repository path
    log.debug('Replacing %s with %s', local_repository, local_repository_temp_destination)
    os.replace(local_repository_temp_destination, local_repository)
    log.info('Checksum for %s was generated and saved to the local repository', updated_file)
    print(f'Checksum for {updated_file} was generated and saved to the local repository...')
    print('...........................................')


def file_update_requester(remote_repository_url, repository_difference_outfile, local_addon_path, local_repository):
    """Requests download of updated file
    """
    log = logger()
    # This file requests files found in repository_difference_outfile
    # Filter out filename of remote repository
    remote_repository_filename = remote_repository_url.split('/')[-1]
    # Remove filename of repository in order to reuse the repository url as a link to the remote addon folder
    remote_addon_path = remote_repository_url.replace(remote_repository_filename, '')
    log.debug('Opening repository difference file from path: %s', repository_difference_outfile)
    with open(repository_difference_outfile, 'r') as repo_diff:
        reader = csv.reader(repo_diff, delimiter='\t')
        for line in reader:
            updated_file = line[0]
            # Sets up the path to the url containing the addon
            updated_file_url = remote_addon_path+line[0]
            # Sets up the path to the url containing the addon
            download_path = local_addon_path+'/'+line[0]
            # Provides the url to addon and addon path to the file_downloader function
            log.info('Requsting download of %s', updated_file_url)
            file_downloader(updated_file_url, download_path)
            log.debug('Updating checksum of %s', updated_file)
            update_checksum(updated_file, local_repository, download_path)
