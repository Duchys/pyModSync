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

#Based on this output addons @ACE, @TFAR, @AGM will be enabled.
#TODO: generate the
import sys
import csv
import hashlib
import os
import shutil

def file_hash_hex(file_path, hash_func):
    with open(file_path, 'rb') as f:
        return hash_func(f.read()).hexdigest()

def sorted_file_listing(base_dir):
    for directory, subdirs, files in sorted(os.walk(base_dir)):
        for filename in files:
            yield os.path.join(directory, filename)

def local_repository_generator(source_addon_directory, checksum_output_destination):
#TODO: Get someone who knows what he is doing, and not just doing CTRL + C from the web until it starts working...



#TODO: add comments so it seems like i know what I'm doing
    checksum_output_temp_destination=checksum_output_destination+'_temp'
    with open(checksum_output_temp_destination, 'w', newline='',encoding='utf-8') as outlocalrepo:
        print('this will take some time, go and grab a coffee')
        writer = csv.writer(outlocalrepo, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for path in sorted_file_listing(source_addon_directory):
            print(path)
            path_processed=path.replace(source_addon_directory,'')
            #Removes / from the path incase the path did not end with a /
            path_processed = path_processed.replace('\\', '/')
            if path_processed.startswith('/'):
                path_processed = path_processed[1:]
            if path_processed.startswith('\\'):
                path_processed = path_processed[1:]
            print (f'Generating checksum for {path_processed}')
            writer.writerow((path_processed, file_hash_hex(path, hashlib.blake2b)))
    shutil.move(checksum_output_temp_destination,checksum_output_destination)
    print(f'Checksum was succesfully generated to {checksum_output_destination}')
    print('...........................................')