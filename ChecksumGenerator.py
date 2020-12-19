#GOAL: Generate initial checksum of the addons
#Take this function
#Point it modpack folder
#provide the following output
#following will be generated /modpack/mod
#example:
#pointed at "offical" modpack folder
#which contains
#@ACE
#@TFAR
#@AGM

#The following will be generated
#official/@ACE
#   official/@ACE/modfilea.pbo  checksum
#   official/@ACE/modfileb.pbo  checksum
#official/@TFAR
#   official/@TFAR/modfilea.pbo checksum
#   official/@TFAR/modfilea.pbo checksum
#official/@AGM
#   official/@AGM/modfilea.pbo checksum
#   official/@AGM/modfilea.pbo checksum

#Based on this output addons @ACE, @TFAR, @AGM will be enabled.
import csv
import hashlib
import os
#TODO: Get someone who knows what he is doing, and not just doing CTRL + C from the web until it starts working...
print('this will take some time, go and grab a coffee')
def file_hash_hex(file_path, hash_func):
    with open(file_path, 'rb') as f:
        return hash_func(f.read()).hexdigest()
#TODO: Get rid of subdirs.
def recursive_file_listing(base_dir):
    for directory, subdirs, files in os.walk(base_dir):
        for filename in files:
            yield directory, filename, os.path.join(directory, filename)
#TODO: take this path from current dir/fitler out unnecessary stuff
#TODO: add comments so it seems like i know what I'm doing
src_dir = '/mnt/ssd/417addons/'
checksum_destination_directory='/tmp/checksums_archive4.csv'
with open(checksum_destination_directory, 'w') as f:
    writer = csv.writer(f, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for directory, filename, path in recursive_file_listing(src_dir):
        writer.writerow((directory, filename, file_hash_hex(path, hashlib.blake2b)))
print(f'Checksum was succesfully generated to {checksum_destination_directory}')