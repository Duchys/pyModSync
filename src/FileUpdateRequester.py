def file_update_requester(remote_repository_url,repository_difference_outfile,local_addon_path):
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
            file_to_download=remote_addon_path+line[0]
            download_path=local_addon_path+'/'+line[0]
            file_downloader(file_to_download,download_path)
            #TODO: Update checksum for each updated file right after download