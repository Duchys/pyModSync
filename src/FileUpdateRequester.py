def update_checksum(updated_file,local_repository,updated_file_path):
    import csv
    import hashlib
    import shutil
    from UserChecksumGenerator import file_hash_hex
    #Read local repository to memory
    with open(local_repository) as inlocalrepo:
        reader = csv.reader(inlocalrepo.readlines(), delimiter='\t')
    

    local_repository_temp_destination=local_repository+'_temp'

    #Create temporary file without the line containing the hash of the updated file
    with open(local_repository_temp_destination, 'w', newline='',encoding='utf-8') as outlocalrepo:
        writer = csv.writer(outlocalrepo, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        print(f'Updating checksum of the {updated_file}')
        for line in reader:
            #If the line does not contain the filaneme of the updated file it will be rewriten to the updated repository
            if not updated_file == line[0]:
                writer.writerow(line)
            else:
                print(f'Line containing {updated_file} found in the local repository, removing the line...')
        #Generate hash for the updated file on the end of the line
        writer.writerow((updated_file, file_hash_hex(updated_file_path, hashlib.blake2b)))
    #Move the temporary repository to the local_repository path
    shutil.move(local_repository_temp_destination,local_repository)
    print (f'Checksum for {updated_file} was generated and saved to the local repository...')
    print('...........................................')


def file_update_requester(remote_repository_url,repository_difference_outfile,local_addon_path,local_repository):
    from FileDownloader import file_downloader
    import csv
    #This file requests files found in repository_difference_outfile
    #Filter out filename of remote repository
    remote_repository_filename=remote_repository_url.split('/')[-1]
    #Remove filename of repository in order to reuse the repository url as a link to the remote addon folder 
    remote_addon_path=remote_repository_url.replace(remote_repository_filename,'')





    with open(repository_difference_outfile,'r') as repo_diff:
        reader = csv.reader(repo_diff, delimiter='\t')
        for line in reader:
            updated_file=line[0]
            #Sets up the path to the url containing the addon
            updated_file_url=remote_addon_path+line[0]
            #Sets up the path to the url containing the addon
            download_path=local_addon_path+'/'+line[0]
            #Provides the url to addon and addon path to the file_downloader function
            file_downloader(updated_file_url,download_path)
            update_checksum(updated_file,local_repository,download_path)
            #TODO: Update checksum for each updated file right after download