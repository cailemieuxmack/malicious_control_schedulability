"""Delay: check task K on every iteration, delayed by b periods. Arbitrary-deadline multiframe RTA with Audsley, C above K.

Writes data/results/delay_{range}_ccr{ccr}.csv with one row per task set:
U, trial, b0, ..., b13, where column b{b} is 1 if the task set is schedulable with D = common.check_deadline(T, b).
Which b is safe for which subset O(y) is decided at plot time (see HANDOFF.md open issue 2).

Usage: python exp_delay.py RANGE CCR     (run_all.sh runs every combination)
"""
import sys

import common
import RTA


def run_one(e, ccr):
    row = {"U": e["U"], "trial": e["trial"]}
    for b in range(common.Y_MAX + 1):
        ts, K, C = common.delay_taskset(e["tasks"], e["control_idx"], ccr, b)
        row[f"b{b}"] = int(RTA.ad_schedulable(ts, check_task=K, control_task=C))
    return row


def run(range_name, ccr):
    rows = [run_one(e, ccr) for e in common.load_tasksets(range_name)]
    common.save_results(rows, common.results_path("delay", range_name, ccr))


if __name__ == "__main__":
    run(sys.argv[1], float(sys.argv[2]))
