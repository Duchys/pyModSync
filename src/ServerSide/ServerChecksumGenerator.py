#GOAL: Generate initial checksum of the addons
#Take this function
#Point it modpack folder and provide .ini file which contains mods you want to be included in the repository
#provide the following output
#following will be generated /modpack/mod
#example:
#pointed at "offical" modpack folder
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
def repository_generator(repository_name, path_to_modlist, source_addon_directory, checksum_output_destination):
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
    #prepares list of mods used in the repository for use in the checksum generator
    modlist = []
    with open(path_to_modlist, 'r') as modlistcsv:
        for row in modlistcsv:
            modlist.append(row)

    modlist_processed = [x[:-1] for x in modlist]

    with open(checksum_output_destination, 'w', newline='',encoding='utf-8') as f:
        print('this will take some time, go and grab a coffee')
        writer = csv.writer(f)
        writer.writerow([repository_name])
        writer.writerow(["#DO NOT INSERT ANYTHING ABOVE THIS LINE"])
        writer = csv.writer(f, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for path in sorted_file_listing(source_addon_directory):
            #Awful hack
            #Prepare string used for validation
            path_validation=path.replace(source_addon_directory,'')
            #If path modified for validation starts with any of strings provided by the modpack.ini file then craete a checksum for it and write it to repository.csv
            if path_validation.startswith(tuple(modlist_processed)):
                writer.writerow((path.replace(source_addon_directory,''), file_hash_hex(path, hashlib.blake2b)))
    print(f'Checksum was succesfully generated to {checksum_output_destination}')

repository_name = '%s' % (sys.argv[1])
path_to_modlist = '%s' % (sys.argv[2])
source_addon_directory = '%s/' % (sys.argv[3])
checksum_output_destination = '%s' % (sys.argv[4])
repository_generator(repository_name, path_to_modlist, source_addon_directory, checksum_output_destination)