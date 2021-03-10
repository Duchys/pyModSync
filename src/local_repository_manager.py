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


def file_hash_hex(file_path, hash_func):
    """Fuction used for hashing
    """
    with open(file_path, 'rb') as file:
        return hash_func(file.read()).hexdigest()


def sorted_file_listing(base_dir):
    """Yeild paths in the provided base_dir
    """
    for directory, subdirs, files in sorted(os.walk(base_dir)):
        for filename in files:
            yield os.path.join(directory, filename)


def local_repository_generator(local_addon_path, checksum_output_destination):
    """Generate local checksum repository which is then used for comparison between local and remote repo
    """
    checksum_output_temp_destination = checksum_output_destination+'_temp'
    with open(checksum_output_temp_destination, 'w', newline='', encoding='utf-8') as outlocalrepo:
        print('this will take some time, go and grab a coffee')
        writer = csv.writer(outlocalrepo, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for path in sorted_file_listing(local_addon_path):
            path_processed = path.replace(local_addon_path, '')
            # Removes / from the path incase the path did not end with a /
            path_processed = path_processed.replace('\\', '/')
            if path_processed.startswith('/'):
                path_processed = path_processed[1:]
            if path_processed.startswith('\\'):
                path_processed = path_processed[1:]
            print(f'Generating checksum for {path_processed}')
            writer.writerow((path_processed, file_hash_hex(path, hashlib.blake2b)))
    shutil.move(checksum_output_temp_destination, checksum_output_destination)
    print(f'Checksum was succesfully generated to {checksum_output_destination}')
    print('...........................................')


def check_for_local_repository(local_addon_path, local_repository):
    """Check if local repository exists
    If not, generate local repository
    """
    # Delete extra / if present
    if local_addon_path.endswith('/'):
        local_addon_path = local_addon_path[:-1]

    print('Checking if local repository already exists')
    print('...........................................')
    # Checks if file local repository already exists, if not it calls the generator to generate the local repository
    if not os.path.isfile(local_repository):
        print('local repository was not found, generating local repository')
        local_repository_generator(local_addon_path, local_repository)
    # Checks if the local repository file is empty, if so, regenerates the local repository
    # This is done in order to prevent redownload of already downloaded files
    # incase some issue arose during the generation of the initial local repository
    elif os.stat(local_repository).st_size == 0:
        print('File exists and is empty, regenerating local repository')
        local_repository_generator(local_addon_path, local_repository)
    else:
        print('File exists and is not empty')
    print('...........................................')
