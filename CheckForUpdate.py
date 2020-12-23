

#TODO: Add comments
def compare_repositories(local_repository, remote_repository_destination_path, repository_difference_outfile):
        with open(local_repository, 'r') as t1, open(remote_repository_destination_path, 'r') as t2:
            file_one = t1.readlines()
            file_two = t2.readlines()

        with open(repository_difference_outfile, 'w') as out_file:
            for line in file_two:
                if line not in file_one:
                    out_file.write(line)

def check_for_update(local_repository, remote_repository_destination_path, repository_difference_outfile):
    compare_repositories(local_repository, remote_repository_destination_path, repository_difference_outfile)
    import os
    if not os.stat(repository_difference_outfile).st_size == 0:
        print ('Change between local and remote repository was detected')
    else:
        
        print ('No change between local and remote repository was detected')
