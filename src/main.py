from check_addons import check_addons
from update_addons import update_addons
from interrupt_handler import interrupt_handler

# Call interupt handler to monitor possible user interuptions
interrupt_handler()

# Download remote repository
# Compare with local repository
# download changed addons
# Compare changed files between local addon repostiory (eg. Franta Cihla's local mod folder [/mnt/addons])
# and remote mod repository (eg. 417RCT Official Repository)

# Check if config file exists, if not create it, then create local addon repository
# After that check for differences between local and remote repository
if check_addons():
    # Update out of date addons based on the output of check_addons function
    update_addons()

print('Addons are up to date.')
