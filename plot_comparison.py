"""Comparison of all approaches (paper Fig 8): fraction of schedulable task sets vs utilization.

- Basic, Naive: as saved.
- Delay: the check delayed for subset O(13). By Eq. 26, D = 13 P, which is column b12.
- Skip: schedulable for at least one y in 1..13.
- Skip & Delay (hybrid): schedulable for at least one (y, a, b) allowed by common.hybrid_allowed.

Usage: python plot_comparison.py [RANGE CCR]     (default: all 16 combinations)
Writes figures/comparison_{range}_ccr{ccr}_{rule}.pdf
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import common
import exp_hybrid

# FIG_DIR = os.path.join(common.HERE, "figures")
FIG_DIR = os.path.join(common.HERE, "drone_figures")
DELAY_B = common.Y_MAX - 1    # Eq. 26 with y* = 13: D = 13 P = check_deadline(P, 12)

SKIP_COLS = [f"y{y}" for y in range(1, common.Y_MAX + 1)]
HYBRID_COLS = [f"y{y}_a{a}_b{b}" for y, a, b in exp_hybrid.combinations() if common.hybrid_allowed(y, a, b)]


def plot(range_name, ccr):
    any_of = common.any_of
    curves = [   # label, rows, schedulable?, linestyle, alpha
        ("Basic", common.load_results("basic", range_name), any_of(["schedulable"]), "-", 1.0),
        ("Naive security", common.load_results("naive", range_name, ccr), any_of(["schedulable"]), "--", 0.85),
        ("Delay (arbitrary deadline)", common.load_results("delay", range_name, ccr), any_of([f"b{DELAY_B}"]), "-.", 0.75),
        ("Skip", common.load_results("skip", range_name, ccr), any_of(SKIP_COLS), ":", 0.9),
        # ("Skip & Delay", common.load_results("hybrid", range_name, ccr), any_of(HYBRID_COLS), (0, (3, 1, 1, 1)), 0.65),
    ]

    plt.figure()
    for label, rows, ok, linestyle, alpha in curves:
        Us, fracs = common.fractions(rows, ok)
        plt.plot(Us, fracs, marker="o", label=label, linestyle=linestyle, alpha=alpha)
        print(f"{range_name:6s} ccr={ccr:<4} {label:27s}", " ".join(f"{f:.2f}" for f in fracs))
    plt.xlabel("Utilization")
    plt.ylabel("Schedulable Fraction")
    plt.legend(loc="lower left")
    plt.grid(alpha=0.3)

    os.makedirs(FIG_DIR, exist_ok=True)
    path = os.path.join(FIG_DIR, f"comparison_{range_name}_ccr{ccr}_{common.HYBRID_RULE}.pdf")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"-> {path}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        plot(sys.argv[1], float(sys.argv[2]))
    else:
        for range_name in common.PERIOD_RANGES:
            for ccr in common.CCRS:
                plot(range_name, ccr)
