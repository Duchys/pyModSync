# pyModSync
tbd
#TODO: advanced options to delete unused files
#TODO: Arma3 Launcher



#Server side
repository .csv file has to be provided in the same place as the directory containing addons (ie. /addons/officialrepository.csv)
To generate the .csv file use the provided ServerChecksumGenerator.exe or run the Python ServerChecksumGenerator.py file.

To launch it you have to provide the following 4 arguments:
1. Repository Name (ie. XY Official Repository)
2. CSV with mods
3. Addon path
4. Repository output destionation

Example command:
Windows: 

```.\ServerChecksumGenerator.exe "Very Cool Repository name" C:\filecontainingmodlist.csv C:\addonfolder C:\pymodsyncrepo.csv``` 

Linux:

```python ServerChecksumGenerator.py "Very Cool Repository name" /srv/pymodsync/filecontainingmodlist.csv /srv/addonfolder /srv/addonfolder/pymodsyncrepo.csv```
