"""Hybrid: starting in O(y), skip a checks, then perform r_inter[y, y - a] checks, each delayed by b periods.
Arbitrary-deadline multiframe RTA with Audsley, C above K.

Writes data/results/hybrid_{range}_ccr{ccr}.csv with one row per task set:
U, trial, and a column y{y}_a{a}_b{b} for every y in 1..13 and a + b <= y, except a = b = 0 (that's the naive check).
A column is 1 if the task set is schedulable with that (y, a, b).
Which (y, a, b) are safe is decided at plot time (see HANDOFF.md open issue 2).

Usage: python exp_hybrid.py RANGE CCR     (run_all.sh runs every combination)
"""
import sys

import common
import RTA


def combinations():
    for y in range(1, common.Y_MAX + 1):
        for a in range(y + 1):
            for b in range(y - a + 1):
                if a == 0 and b == 0:
                    continue
                yield y, a, b


def run_one(e, ccr, r_inter):
    row = {"U": e["U"], "trial": e["trial"]}
    for y, a, b in combinations():
        ts, K, C = common.hybrid_taskset(e["tasks"], e["control_idx"], ccr, r_inter, y, a, b)
        row[f"y{y}_a{a}_b{b}"] = int(RTA.ad_schedulable(ts, check_task=K, control_task=C))
    return row


def run(range_name, ccr):
    r_inter = common.load_inter_onions()
    rows = [run_one(e, ccr, r_inter) for e in common.load_tasksets(range_name)]
    common.save_results(rows, common.results_path("hybrid", range_name, ccr))


if __name__ == "__main__":
    run(sys.argv[1], float(sys.argv[2]))
