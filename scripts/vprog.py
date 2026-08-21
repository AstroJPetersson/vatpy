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
from tqdm import tqdm


def get_max_time(sim_dir):
    pattern = re.compile(r'TimeMax\s*([^,;\s]+)')

    with open(sim_dir + '/Arepo.out', 'r') as file:
        lines = file.readlines()
        for line in lines:
            match = pattern.search(line)
            if match:
                time = float(match.group(1))
                break

    return time


def get_current_time(sim_dir):
    pattern = re.compile(r'Time: ([^,;\s]+)')

    with open(sim_dir + '/Arepo.out', 'r') as file:
        lines = file.readlines()
        for line in lines[::-1]:
            match = pattern.search(line)
            if match:
                time = float(match.group(1))
                break

    return time


# -------------- Run script
def main() -> None:
    # Search for directories:
    dir_list = os.listdir(os.getcwd())

    # Initialize progress bars
    progress_bars = {}
    for sim in dir_list:
        max_time = get_max_time(sim)
        progress_bars[sim] = tqdm(
            total=max_time,
            desc=sim,
            unit="s",
            position=len(progress_bars),
            leave=True,
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}"
        )

    # Monitor progress
    remaining = set(dir_list)
    while remaining:
        for sim in list(remaining):
            current_time = get_current_time(sim)
            progress_bars[sim].n = current_time
            progress_bars[sim].refresh()

            if current_time >= progress_bars[sim].total:
                progress_bars[sim].close()
                remaining.remove(sim)

        time.sleep(1)  # Update every second


if __name__ == '__main__':
    main()

# -------------- End of file
