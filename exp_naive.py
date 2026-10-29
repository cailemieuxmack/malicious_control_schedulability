"""Naive: check task K on every iteration, inserted directly after the control task C. Implicit-deadline RTA.

Writes data/results/naive_{range}_ccr{ccr}.csv with one row per task set: U, trial, schedulable.

Usage: python exp_naive.py RANGE CCR     (run_all.sh runs every combination)
"""
import sys

import common
import RTA


def run(range_name, ccr):
    rows = []
    for e in common.load_tasksets(range_name):
        ts = common.naive_taskset(e["tasks"], e["control_idx"], ccr)
        rows.append({"U": e["U"], "trial": e["trial"], "schedulable": int(RTA.schedulable(ts))})
    common.save_results(rows, common.results_path("naive", range_name, ccr))


if __name__ == "__main__":
    run(sys.argv[1], float(sys.argv[2]))
