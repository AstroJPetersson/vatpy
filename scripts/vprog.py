# Description: TODO
# Authour(s): Jonathan Petersson
# Last updated: 2026-08-21


# -------------- Required Packages
import os
import re
import sys
import time
import random
import progressbar


def get_max_time(sim_dir):
    pattern = re.compile(r'TimeMax\s*([^,;\s]+)')

    with open(sim_dir + '/Arepo.out', 'r') as file:
        lines = file.readlines()
        for line in lines:
            match = pattern.search(line)
            if match:
                time = match.group(1)
                break

    return time


def get_current_time(sim_dir):
    pattern = re.compile(r'Time: ([^,;\s]+)')

    with open(sim_dir + '/Arepo.out', 'r') as file:
        lines = file.readlines()
        for line in lines[::-1]:
            match = pattern.search(line)
            if match:
                time = match.group(1)
                break

    return time


# -------------- Run script
# Search for directories:
dir_list = os.listdir(os.getcwd())

SIM_MAX_TIME = {}
for sim in dir_list:
    SIM_MAX_TIME[sim] = get_max_time(sim)

SIM_CURRENT_TIME = {}
for sim in dir_list:
    SIM_CURRENT_TIME[sim] = get_current_time(sim)


def main() -> None:
    with progressbar.MultiBar(fd=sys.stdout) as multibar:
        for sim, total in SIM_MAX_TIME.items():
            multibar[sim].max_value = total

        remaining = dict(SIM_CURRENT_TIME)
        while remaining:
            sim = random.choice(list(remaining))
            multibar[sim].value = get_current_time(sim)
            if multibar[sim].value >= multibar[sim].max_value:
                multibar[sim].finish()
                del remaining[sim]
            time.sleep(0.01)


if __name__ == '__main__':
    main()

# -------------- End of file
