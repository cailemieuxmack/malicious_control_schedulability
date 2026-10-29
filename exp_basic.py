"""Basic: the task set without any check task. Implicit-deadline RTA, RM priority.

Writes data/results/basic_{range}.csv with one row per task set: U, trial, schedulable.
Doesn't depend on the CCR.

Usage: python exp_basic.py RANGE     (run_all.sh runs every range)
"""
import sys

import common
import RTA


def run(range_name):
    rows = []
    for e in common.load_tasksets(range_name):
        ts = common.basic_taskset(e["tasks"])
        rows.append({"U": e["U"], "trial": e["trial"], "schedulable": int(RTA.schedulable(ts))})
    common.save_results(rows, common.results_path("basic", range_name))


if __name__ == "__main__":
    run(sys.argv[1])
