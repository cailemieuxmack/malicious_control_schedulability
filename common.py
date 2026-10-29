"""Shared parameters, data loading and task-set builders for the schedulability experiments.

A task is (frames, T) for implicit deadlines or (frames, T, D) for arbitrary deadlines.
C is the control task, K is the check task. K always has the same period as C and lower priority.
"""
import csv
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "drone_data")

########## Experiment parameters (paper defaults) ##########

UTILIZATIONS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
N_MAX = 20            # number of tasks is random.randint(1, N_MAX)
TRIALS = 800          # task sets per utilization point

PERIOD_RANGES = {     # microseconds
    "small": (3000, 30000),
    "medium": (10000, 100000),
    "large": (50000, 250000),
    "wide": (3000, 250000),
}
SEEDS = {"small": 1, "medium": 2, "large": 3, "wide": 4}

CCRS = [0.1, 0.4, 1.0, 2.0]   # check cost ratio: cost(K) = ceil(cost(C) * CCR)

########## Inverted pendulum bounds ##########

# Y_MAX = 13            # subsets O(0) .. O(13)
Y_MAX = 4
# Constrained bound r*(y), used by the skip approach.
# TRADEOFFS = [0, 7, 15, 20, 23, 28, 33, 35, 34, 37, 36, 38, 37, 35]
TRADEOFFS = [0, 49, 61, 53, 44]

# Unconstrained bound read off paper Fig 4b, only used to sanity check the inter_onions conversion.
UNCONSTRAINED_BOUND = [0, 8, 22, 28, 37, 42, 53, 63, 73, 82, 92, 103, 116, 135]

INTER_ONIONS_FILE = os.path.join(HERE, "inverted_pendulum_inter_onions.npy")
INTER_ONIONS_SCALE = 5   # the .npy file is stored at 5x the control-loop resolution


def load_inter_onions(path=INTER_ONIONS_FILE, scale=INTER_ONIONS_SCALE):
    """r_inter[target, start]: control-loop iterations to get from O(start) to O(target).

    The stored values are at `scale` times the control-loop resolution, so we divide by scale and take the ceiling.
    """
    raw = np.load(path)
    r_inter = np.ceil(raw / scale).astype(int)
    for y in range(Y_MAX + 1):
        assert r_inter[y, 0] == UNCONSTRAINED_BOUND[y], f"inter_onions[{y}, 0] = {r_inter[y, 0]}, expected {UNCONSTRAINED_BOUND[y]}"
    return r_inter

########## Paths ##########

def tasksets_path(range_name):
    return os.path.join(DATA_DIR, "tasksets", f"{range_name}.json")


def results_path(analysis, range_name, ccr=None):
    """ccr=None for analyses that don't depend on the check cost (basic)."""
    name = f"{analysis}_{range_name}" if ccr is None else f"{analysis}_{range_name}_ccr{ccr}"
    return os.path.join(DATA_DIR, "results", f"{name}.csv")


def save_results(rows, path):
    """rows: list of dicts with the same keys, one per task set."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} rows -> {path}")


def load_results(analysis, range_name, ccr=None):
    """List of dicts, one per task set. All values are strings, as read from the CSV."""
    with open(results_path(analysis, range_name, ccr), newline="") as f:
        return list(csv.DictReader(f))


def any_of(cols):
    """For fractions(): a row counts as schedulable if any of these columns is 1."""
    return lambda row: any(row[c] == "1" for c in cols)


def fractions(rows, ok):
    """Fraction of rows with ok(row) per utilization. Returns (U values, fractions)."""
    total, accepted = {}, {}
    for row in rows:
        U = float(row["U"])
        total[U] = total.get(U, 0) + 1
        accepted[U] = accepted.get(U, 0) + int(ok(row))
    Us = sorted(total)
    return Us, [accepted[U] / total[U] for U in Us]


def load_tasksets(range_name):
    """List of dicts with keys U, trial, tasks ([[cost, period], ...], RM sorted) and control_idx."""
    with open(tasksets_path(range_name)) as f:
        return json.load(f)["tasksets"]

########## Deadline of a delayed check ##########

def check_deadline(P, b):
    """Deadline of a check delayed by b periods on top of its original deadline P."""
    return (b + 1) * P

########## Which delayed checks are safe (applied at plot time) ##########

# UNRESOLVED, see HANDOFF.md open issue 2.
#   "theorem1": a + b <= y, as paper Theorem 1 is written. The old figures used this.
#   "eq26":     a + b + 1 <= y when b >= 1. By the Eq. 26 argument, a check delayed b periods lets b + 1 malicious actions through.
HYBRID_RULE = "theorem1"


def hybrid_allowed(y, a, b, rule=HYBRID_RULE):
    """Is skipping a checks and delaying the rest by b periods safe when starting in O(y)?"""
    if b == 0:
        return a <= y    # undelayed checks block their own iteration's action
    if rule == "theorem1":
        return a + b <= y
    if rule == "eq26":
        return a + b + 1 <= y
    raise ValueError(f"unknown rule {rule}")

########## Task-set builders, one per approach ##########

def check_cost(tasks, control_idx, ccr):
    return math.ceil(tasks[control_idx][0] * ccr)


def multiframe(tasks):
    """[[cost, period], ...] -> [([cost], period), ...]"""
    return [([c], T) for c, T in tasks]


def basic_taskset(tasks):
    return multiframe(tasks)


def naive_taskset(tasks, control_idx, ccr):
    """Check K on every iteration, inserted directly after C."""
    ts = multiframe(tasks)
    T = tasks[control_idx][1]
    ts.insert(control_idx + 1, ([check_cost(tasks, control_idx, ccr)], T))
    return ts


def skip_taskset(tasks, control_idx, ccr, y):
    """Skip y checks, then perform TRADEOFFS[y] checks. Frames start with the checks so C0 = Cm."""
    ts = multiframe(tasks)
    T = tasks[control_idx][1]
    c = check_cost(tasks, control_idx, ccr)
    ts.insert(control_idx + 1, ([c] * TRADEOFFS[y] + [0] * y, T))
    return ts


def arbitrary_deadline(tasks):
    """[[cost, period], ...] -> [([cost], period, period), ...]"""
    return [([c], T, T) for c, T in tasks]


def delay_taskset(tasks, control_idx, ccr, b):
    """Check on every iteration, delayed by b periods.

    Returns (ts, K, C). Call RTA.ad_schedulable(ts, check_task=K, control_task=C); K and C are the objects inside ts.
    """
    ts = arbitrary_deadline(tasks)
    T = tasks[control_idx][1]
    K = ([check_cost(tasks, control_idx, ccr)], T, check_deadline(T, b))
    ts.insert(control_idx + 1, K)
    return ts, K, ts[control_idx]


def hybrid_taskset(tasks, control_idx, ccr, r_inter, y, a, b):
    """Starting in O(y): skip a checks, then perform r_inter[y, y - a] checks, each delayed by b periods.

    With a = 0 there are no skips and this is the plain delayed check.
    Returns (ts, K, C), as delay_taskset.
    """
    ts = arbitrary_deadline(tasks)
    T = tasks[control_idx][1]
    c = check_cost(tasks, control_idx, ccr)
    if a == 0:
        frames = [c]
    else:
        n_checks = int(r_inter[y, y - a])
        assert n_checks >= 1
        frames = [c] * n_checks + [0] * a
    K = (frames, T, check_deadline(T, b))
    ts.insert(control_idx + 1, K)
    return ts, K, ts[control_idx]
