"""Generate the task sets for every period range and save them to data/tasksets/{range}.json.

The same task sets and control task are used for all approaches and all CCRs.

Usage: python generate_tasksets.py [range ...]     (default: all ranges)
"""
import json
import os
import random
import sys

import common
import generate_better


def generate(range_name):
    T_min, T_max = common.PERIOD_RANGES[range_name]
    random.seed(common.SEEDS[range_name])

    tasksets = []
    for U in common.UTILIZATIONS:
        for trial in range(common.TRIALS):
            ts = generate_better.generate_taskset(random.randint(1, common.N_MAX), U, T_min, T_max)
            ts_rm = sorted(ts, key=lambda x: x[1])    # rate monotonic: list order is priority order
            control_idx = random.randint(0, len(ts_rm) - 1)
            tasksets.append({
                "U": U,
                "trial": trial,
                "tasks": [[c, T] for c, T in ts_rm],
                "control_idx": control_idx,
            })

    path = common.tasksets_path(range_name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump({
            "range": range_name,
            "T_min": T_min,
            "T_max": T_max,
            "seed": common.SEEDS[range_name],
            "tasksets": tasksets,
        }, f)
    print(f"{range_name}: {len(tasksets)} task sets -> {path}")


if __name__ == "__main__":
    for range_name in sys.argv[1:] or common.PERIOD_RANGES:
        generate(range_name)
