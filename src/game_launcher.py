import os
import subprocess
import traceback
from config_manager import config_loader
from config_manager import check_if_config_exists


def game_launcher():
    """Launch arma with mods as an optional parameter
    """
    # Load configuration
    check_if_config_exists()
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
    # Add backslash to addon path
    local_addon_path_processed = local_addon_path + '/'
    # Adds full addon path to the modpath
    mod_list = [local_addon_path_processed + s for s in mod_list]
    # Starts the Arma 3 with optional addons
    # Check if it is Windows
    if os.name == 'nt':
        steam_exe_path = config[5]
        mod_list = [s.replace('/', '\\') for s in mod_list]
        launch_command = (f"\"{steam_exe_path}\" -applaunch 107410 -nolauncher -mod='{';'.join(mod_list)}'")
        try:
            subprocess.run(launch_command, shell=True, check=True)
        except subprocess.CalledProcessError:
            print('Launching of Arma 3 failed')
            print('Failed command:')
            print(launch_command)
            trace_back = traceback.format_exc()
            print(trace_back)
            exit(1)
    else:
        proton_mnt_drive_letter = 'Z:'
        # Add proton mount drive letter to each string in list
        mod_list = [proton_mnt_drive_letter + s for s in mod_list]
        # Replace / with \\ for correct addon loading
        mod_list = [s.replace('/', '\\') for s in mod_list]
        launch_command = (f"steam -applaunch 107410 -mod='{';'.join(mod_list)}'")
        try:
            subprocess.run(launch_command, shell=True, check=True)
        except subprocess.CalledProcessError:
            print('Launching of Arma 3 failed')
            print('Failed command:')
            print(launch_command)
            trace_back = traceback.format_exc()
            print(trace_back)
            exit(1)


game_launcher()
