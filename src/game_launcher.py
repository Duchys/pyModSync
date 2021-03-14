import subprocess
from config_manager import config_loader


def game_launcher():
    """Launch arma with mods as an optional parameter
    """
    # Load configuration
    config = config_loader()
    remote_repository = config[3]
    local_addon_path = config[4]
    # Prepare list
    mod_list = []
    # Open remote repostiory
    with open(remote_repository, 'r') as remote_repo:
        # Skips first 2 lines
        remote_repo = remote_repo.readlines()[2:]
        # For every line in remote repository
        # Read the first part of the line, until / is reached
        # Then save it to a list
        for line in remote_repo:
            mod = (line.rsplit('/')[0])
            mod_list.append(mod)
    # Remove duplicite lines
    mod_list = list(set(mod_list))
    # URL parsing
    mod_list = [x.replace('@', '%40') for x in mod_list]
    # Add backslash to addon path
    local_addon_path_processed = local_addon_path + '/'
    # URL parsing
    local_addon_path_processed = local_addon_path_processed.replace("/", "%2F")
    # Adds full addon path to the modpath
    mod_list = [local_addon_path_processed + s for s in mod_list]
    # Starts the Arma 3 with optional addons
    subprocess.run(f"steam steam://rungameid/107410//-mod={'%3B'.join(mod_list)}", shell=True, check=True)

# Windows to be tested
# subprocess.run("cmd /c start steam://rungameidm/107410")


game_launcher()
