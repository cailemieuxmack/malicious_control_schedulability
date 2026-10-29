"""Skip: starting in O(y), skip y checks, then perform TRADEOFFS[y] checks. Implicit-deadline multiframe RTA.

Writes data/results/skip_{range}_ccr{ccr}.csv with one row per task set:
U, trial, y1, ..., y13, where column y{y} is 1 if the task set is schedulable when skipping with subset O(y).

Usage: python exp_skip.py RANGE CCR     (run_all.sh runs every combination)
"""
import sys

import common
import RTA


def run(range_name, ccr):
    rows = []
    for e in common.load_tasksets(range_name):
        row = {"U": e["U"], "trial": e["trial"]}
        for y in range(1, common.Y_MAX + 1):
            ts = common.skip_taskset(e["tasks"], e["control_idx"], ccr, y)
            row[f"y{y}"] = int(RTA.schedulable(ts))
        rows.append(row)
    common.save_results(rows, common.results_path("skip", range_name, ccr))


if __name__ == "__main__":
    run(sys.argv[1], float(sys.argv[2]))
