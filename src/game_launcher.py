import os
import subprocess
import traceback
import sys
from config_manager import config_loader
from config_manager import check_if_config_exists
from logger import logger


def get_modlist():
    """Processes mod list from remote repository file
    and based on them modl ist create a list with local addon paths.
    """
    log = logger()
    # Prepare list
    mod_list = []
    check_if_config_exists()
    config = config_loader()
    remote_repository = config[3]
    local_addon_path = config[4]
    log.debug('Opening remote repository from path: %s', remote_repository)
    log.debug('Reading mod list')
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
    log.debug('Processing mod list to remove duplicate lines')
    mod_list = list(set(mod_list))
    log.debug('Mod list: %s', mod_list)
    # Add backslash to addon path
    local_addon_path_processed = local_addon_path + '/'
    # Adds full addon path to the modpath
    mod_list = [local_addon_path_processed + s for s in mod_list]
    log.debug('Local paths to addons in modpath: %s', local_addon_path_processed)
    return mod_list


def game_launch_failed(launch_command):
    """Output and logging, when launch of Arma 3 fails
    """
    log = logger()
    print('Launching of Arma 3 failed.')
    log.error('Launchingf of Arma 3 failed')
    log.error('Launch command: %s', launch_command)
    trace_back = traceback.format_exc()
    log.error(trace_back)
    sys.exit(trace_back)


def game_launcher():
    """Launch arma with mods as an optional parameter
    """
    log = logger()
    config = config_loader()
    # Load configuration
    mod_list = get_modlist()
    # Starts the Arma 3 with optional addons
    # Check if it is Windows
    if os.name == 'nt':
        log.debug('Windows detected.')
        steam_exe_path = config[5]
        # Replace / with \\ for correct addon loading
        mod_list = [s.replace('/', '\\') for s in mod_list]
        # Prepare launch command
        launch_command = (f"\"{steam_exe_path}\" -applaunch 107410 -nolauncher -mod='{';'.join(mod_list)}'")
        log.debug('Game launch command prepared: %s', launch_command)
        # Try launching Arma 3
        try:
            subprocess.run(launch_command, shell=True, check=True)
        except subprocess.CalledProcessError:
            game_launch_failed(launch_command)
    else:
        log.debug('Linux detected.')
        proton_mnt_drive_letter = 'Z:'
        # Add proton mount drive letter to each string in list
        mod_list = [proton_mnt_drive_letter + s for s in mod_list]
        # Replace / with \\ for correct addon loading
        mod_list = [s.replace('/', '\\') for s in mod_list]
        log.debug('mod list prepared as: %s', mod_list)
        # Prepare launch command
        launch_command = (f"steam -applaunch 107410 -mod='{';'.join(mod_list)}'")
        log.debug('Game launch command prepared: %s', launch_command)
        # Attempt to launch Arma 3
        try:
            subprocess.run(launch_command, shell=True, check=True)
        # In case it print traceback and exit
        except subprocess.CalledProcessError:
            game_launch_failed(launch_command)


game_launcher()
