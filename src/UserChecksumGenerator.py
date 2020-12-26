#GOAL: Generate initial checksum of local addon folder
#Take this function
#Point it folder containing addons
#provide the following output
#example:
#pointed at local modpack folder
#which contains
#@ACE
#@TFAR
#@AGM

#The following will be generated
#@ACE/modfilea.pbo  checksum
#@ACE/modfileb.pbo  checksum
#@TFAR/modfilea.pbo checksum
#@TFAR/modfilea.pbo checksum
#@AGM/modfilea.pbo checksum
#@AGM/modfilea.pbo checksum
import sys
#Based on this output addons @ACE, @TFAR, @AGM will be enabled.
def local_repository_generator(source_addon_directory, checksum_output_destination):
    import csv
    import hashlib
    import os
#TODO: Get someone who knows what he is doing, and not just doing CTRL + C from the web until it starts working...

    def file_hash_hex(file_path, hash_func):
        with open(file_path, 'rb') as f:
            return hash_func(f.read()).hexdigest()
    def sorted_file_listing(base_dir):
        for directory, subdirs, files in sorted(os.walk(base_dir)):
            for filename in files:
                yield os.path.join(directory, filename)
#TODO: add comments so it seems like i know what I'm doing
    with open(checksum_output_destination, 'w', newline='',encoding='utf-8') as f:
        print('this will take some time, go and grab a coffee')
        writer = csv.writer(f)
        writer = csv.writer(f, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for path in sorted_file_listing(source_addon_directory):
            path_processed=path.replace(source_addon_directory,'')
            #Removes / from the path incase the path did not end with a /
            if path.startswith('/'):
                path_processed = path_processed[1:]
            if path.startswith('\\'):
                path_processed = path_processed[1:]
            path_processed = path_processed.replace(os.sep, '/')
            writer.writerow((path_processed, file_hash_hex(path, hashlib.blake2b)))
    print(f'Checksum was succesfully generated to {checksum_output_destination}')