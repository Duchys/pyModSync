

#TODO: Add comments
#Repository comparison
def compare_repositories(local_repository, remote_repository_destination_path, repository_difference_outfile):
        #Opens repo csv files
        with open(local_repository, 'r') as t1:
            local_repo = t1.readlines()
            #skips first 2 lines
        with open(remote_repository_destination_path, 'r') as t2:
            remote_repo = t2.readlines()[2:]
        #Compares local repository with remote repostitory
        with open(repository_difference_outfile, 'w') as repo_diff:
            #Each line present in remote repostiory gets compared to the local_repository. If the line is not present (ie. not exact match) it gets put to a repo_diff .csv file.
            for line in remote_repo:
                if line not in local_repo:
                    repo_diff.write(line)

#Checks if there is any difference between repositories based on output of compare_repositories
def check_for_update(local_repository, remote_repository_destination_path, repository_difference_outfile):
    compare_repositories(local_repository, remote_repository_destination_path, repository_difference_outfile)
    import os
    if not os.stat(repository_difference_outfile).st_size == 0:
        print ('Change between local and remote repository was detected')
        return 1
    else:
        print ('No change between local and remote repository was detected')
        print('...........................................')
        return 0
        