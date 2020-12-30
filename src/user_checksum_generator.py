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
            yield subdirs, os.path.join(directory, filename)


def local_repository_generator(source_addon_directory, checksum_output_destination):
    """Generate local checksum repository which is then used for comparison between local and remote repo
    """
    checksum_output_temp_destination = checksum_output_destination+'_temp'
    with open(checksum_output_temp_destination, 'w', newline='', encoding='utf-8') as outlocalrepo:
        print('this will take some time, go and grab a coffee')
        writer = csv.writer(outlocalrepo, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for path in sorted_file_listing(source_addon_directory):
            path_processed = path.replace(source_addon_directory, '')
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
