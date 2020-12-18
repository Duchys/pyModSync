#GOAL: The point of this file is to compare the local files with the files provided by the repository
#After a change is found provide it to the FileDownloader which will download then download the file
#If a file is missing, provide the link to the file to the FileDownloader

#Possible checks:
#checksum (preffered, currently not provided by the Almighty Arcanum)
#filesize (cannot be the only check for file change as it is not 100% way to check for file difference)
#modifytime (currently provided by the Almighty Arcanum) >>> Verify if this can be compared with the old repository xml file
