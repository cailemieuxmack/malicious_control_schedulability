"""Tradeoff plots (paper Fig 9): fraction of schedulable task sets vs utilization, one curve per parameter value.

- delay:     one curve per subset O(y), y = 1..13, with the check delayed by Eq. 26: D = y P (column b{y-1}).
- hybrid_y*: subset O(y) fixed (HYBRID_YS), one curve per number of skips a = 1..y,
             with the largest delay b that common.hybrid_allowed permits (b = y - a under theorem1).

Usage: python plot_tradeoffs.py [RANGE CCR]     (default: all 16 combinations; the paper shows medium 2.0)
Writes figures/delay_{range}_ccr{ccr}.pdf and figures/hybrid_y{y}_{range}_ccr{ccr}_{rule}.pdf
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import common

# FIG_DIR = os.path.join(common.HERE, "figures")
FIG_DIR = os.path.join(common.HERE, "drone_figures")
# HYBRID_YS = [13, 6]    # paper Fig 9b, 9c


def max_delay(y, a):
    """Largest b allowed when starting in O(y) and skipping a checks."""
    return max(b for b in range(y - a + 1) if common.hybrid_allowed(y, a, b))


def plot_curves(curves, path):
    """curves: list of (label, Us, fractions). Colors follow matplotlib's default cycle, as in the paper."""
    plt.figure()
    for label, Us, fracs in curves:
        plt.plot(Us, fracs, marker="o", markersize=3, label=label)
    plt.xlabel("Utilization")
    plt.ylabel("Schedulable Fraction")
    plt.legend(loc="lower left", fontsize="small")
    plt.grid(alpha=0.3)
    os.makedirs(FIG_DIR, exist_ok=True)
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"-> {path}")


def plot_delay(range_name, ccr):
    rows = common.load_results("delay", range_name, ccr)
    curves = []
    for y in range(1, common.Y_MAX + 1):
        Us, fracs = common.fractions(rows, common.any_of([f"b{y - 1}"]))
        curves.append((f"Delayed {y} iteration{'s' if y > 1 else ''}", Us, fracs))
    plot_curves(curves, os.path.join(FIG_DIR, f"delay_{range_name}_ccr{ccr}.pdf"))


def plot_hybrid(range_name, ccr, y):
    rows = common.load_results("hybrid", range_name, ccr)
    curves = []
    for a in range(1, y + 1):
        b = max_delay(y, a)
        Us, fracs = common.fractions(rows, common.any_of([f"y{y}_a{a}_b{b}"]))
        curves.append((f"Skipped {a}, delayed {b}", Us, fracs))
    plot_curves(curves, os.path.join(FIG_DIR, f"hybrid_y{y}_{range_name}_ccr{ccr}_{common.HYBRID_RULE}.pdf"))


def plot(range_name, ccr):
    plot_delay(range_name, ccr)
    for y in HYBRID_YS:
        plot_hybrid(range_name, ccr, y)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        plot(sys.argv[1], float(sys.argv[2]))
    else:
        for range_name in common.PERIOD_RANGES:
            for ccr in common.CCRS:
                plot(range_name, ccr)
