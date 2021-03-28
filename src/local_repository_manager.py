# GOAL: Generate initial checksum of local addon folder
# Take this function
# Point it folder containing addons
# provide the following output
# example:
# pointed at local modpack folder
# which contains
# @ACE
# @TFAR
# @AGM

# The following will be generated
# @ACE/modfilea.pbo  checksum
# @ACE/modfileb.pbo  checksum
# @TFAR/modfilea.pbo checksum
# @TFAR/modfilea.pbo checksum
# @AGM/modfilea.pbo checksum
# @AGM/modfilea.pbo checksum

# Based on this output addons @ACE, @TFAR, @AGM will be enabled.
import csv
import hashlib
import os
import shutil
from logger import logger


def file_hash_hex(file_path, hash_func):
    """Fuction used for hashing
    """
    # Read the binary hex of the file (I guess?)
    with open(file_path, 'rb') as file:
        return hash_func(file.read()).hexdigest()


def sorted_file_listing(base_dir):
    """Yeild paths in the provided base_dir
    """
    # Read all of the directories, subdirectories and files in the provided path
    for directory, subdirs, files in sorted(os.walk(base_dir)):
        for filename in files:
            yield os.path.join(directory, filename)


def local_repository_generator(local_addon_path, checksum_output_destination):
    """Generate local checksum repository which is then used for comparison between local and remote repo
    """
    log = logger()
    checksum_output_temp_destination = checksum_output_destination+'_temp'
    log.debug('Checksum temporary output destination set to %s', checksum_output_temp_destination)

    # Open temporary checksum file for writing
    log.debug('Opening checksum temp file for writing')
    with open(checksum_output_temp_destination, 'w', newline='', encoding='utf-8') as outlocalrepo:
        print('this will take some time, go and grab a coffee')
        writer = csv.writer(outlocalrepo, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # for path returned frm sorted_file_listing function
        # generate a checksum
        for path in sorted_file_listing(local_addon_path):
            path_processed = path.replace(local_addon_path, '')
            # Removes / from the path incase the path did not end with a /
            path_processed = path_processed.replace('\\', '/')
            if path_processed.startswith('/'):
                path_processed = path_processed[1:]
            if path_processed.startswith('\\'):
                path_processed = path_processed[1:]
            # Generate checksum for file
            log.debug('Generating checksum for %s', path_processed)
            print(f'Generating checksum for {path_processed}')
            writer.writerow((path_processed, file_hash_hex(path, hashlib.blake2b)))
    # Move temporary checksum file to the final checksum destination
    log.debug('Moving temporary checksum file to: %s', checksum_output_destination)
    shutil.move(checksum_output_temp_destination, checksum_output_destination)
    print(f'Checksum was succesfully generated to {checksum_output_destination}')
    print('...........................................')


def check_for_local_repository(local_addon_path, local_repository):
    """Check if local repository exists
    If not, generate local repository
    """
    log = logger()
    # Delete extra / if present
    if local_addon_path.endswith('/'):
        local_addon_path = local_addon_path[:-1]
    log.info('Checking if local repository exists')
    print('Checking if local repository exists')
    print('...........................................')
    # Checks if file local repository already exists, if not it calls the generator to generate the local repository
    if not os.path.isfile(local_repository):
        log.info('Local repository was not found, generating local repository')
        print('Local repository was not found, generating local repository')
        local_repository_generator(local_addon_path, local_repository)
    # Checks if the local repository file is empty, if so, regenerates the local repository
    # This is done in order to prevent redownload of already downloaded files
    # incase some issue arose during the generation of the initial local repository
    elif os.stat(local_repository).st_size == 0:
        log.info('Local repository is empty, regenerating local repository')
        print('File exists and is empty, regenerating local repository')
        local_repository_generator(local_addon_path, local_repository)
    else:
        log.info('Local repository found and is not empty')
        print('Local repository exists and is not empty')
    print('...........................................')
