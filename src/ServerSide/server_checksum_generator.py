# GOAL: Generate initial checksum of the addons
# Take this function
# Point it modpack folder and provide .ini file
# which contains mods you want to be included in the repository
# provide the following output
# following will be generated /modpack/mod
# example:
# pointed at "offical" modpack folder
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
import sys
import csv
import hashlib
import os

# Generate server repository containing addons
# based on the provided modlist and source addon directory


def sorted_file_listing(base_dir):
    """Yeild paths in the provided base_dir
    """
    for directory, subdirs, files in sorted(os.walk(base_dir)):
        for filename in files:
            yield os.path.join(directory, filename)


def file_hash_hex(file_path, hash_func):
    """Fuction used for hashing
    """
    with open(file_path, 'rb') as file:
        return hash_func(file.read()).hexdigest()


def remote_repository_generator():
    """Generate server repository
    """

    # prepares list of mods used in the repository for use in the checksum generator
    modlist = []
    with open(path_to_modlist, 'r', encodinf='utf-8') as modlistcsv:
        for row in modlistcsv:
            modlist.append(row)

    modlist_processed = [x[:-1] for x in modlist]

    with open(checksum_output_destination, 'w', newline='', encoding='utf-8') as checksum_outfile:
        print('this will take some time, go and grab a coffee')
        writer = csv.writer(checksum_outfile)
        writer.writerow([repository_name])
        writer.writerow(["#DO NOT INSERT ANYTHING ABOVE THIS LINE"])
        writer = csv.writer(checksum_outfile, delimiter='\t',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for path in sorted_file_listing(source_addon_directory):
            # Prepare string used for validation
            path_processed = path.replace(source_addon_directory, '')
            if path_processed.startswith('/'):
                path_processed = path_processed[1:]
            if path.startswith('\\'):
                path_processed = path_processed[1:]
            path_processed = path_processed.replace('\\', '/')
            # If path modified for validation starts with any of strings
            # provided by the modpack.ini file
            # then craete a checksum for it and write it to repository.csv
            if path_processed.startswith(tuple(modlist_processed)):
                # Removes / from the path incase the path did not end with a /
                print(f'Generating checksum for {path_processed}')
                writer.writerow((path_processed, file_hash_hex(path, hashlib.blake2b)))
        print(f'Checksum was succesfully generated to {checksum_output_destination}')


repository_name = '%s' % (sys.argv[1])
path_to_modlist = '%s' % (sys.argv[2])
source_addon_directory = '%s/' % (sys.argv[3])
checksum_output_destination = '%s' % (sys.argv[4])
remote_repository_generator()
