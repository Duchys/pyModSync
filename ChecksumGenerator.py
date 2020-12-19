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
def RepositoryGenerator(repository_name, source_addon_directory, checksum_output_destination):
    import csv
    import hashlib
    import os
#TODO: Get someone who knows what he is doing, and not just doing CTRL + C from the web until it starts working...

    def file_hash_hex(file_path, hash_func):
        with open(file_path, 'rb') as f:
            return hash_func(f.read()).hexdigest()
#TODO: Get rid of subdirs.
    def sorted_file_listing(base_dir):
        for directory, subdirs, files in sorted(os.walk(base_dir)):
            for filename in files:
                yield directory, filename, os.path.join(directory, filename)
#TODO: add comments so it seems like i know what I'm doing
    with open(checksum_output_destination, 'w') as f:
        print('this will take some time, go and grab a coffee')
        writer = csv.writer(f)
        writer.writerow([repository_name])
        writer.writerow(["#DO NOT INSERT ANYTHING ABOVE THIS LINE"])
        writer = csv.writer(f, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for directory, filename, path in sorted_file_listing(source_addon_directory):
            writer.writerow((directory.replace(source_addon_directory,''), filename, file_hash_hex(path, hashlib.blake2b)))
    print(f'Checksum was succesfully generated to {checksum_output_destination}')

repository_name = '417RCT Official Repository'
source_addon_directory = '/mnt/ssd/417addons/'
checksum_output_destination = '/tmp/checksums_archive5.csv'
RepositoryGenerator(repository_name, source_addon_directory, checksum_output_destination)
