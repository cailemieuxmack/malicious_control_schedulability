#!/bin/bash
# Run every experiment for every period range and CCR, one process per combination.
#
# Usage: ./run_all.sh [EXPERIMENT ...]     (default: all of hybrid delay skip naive basic)
#   e.g. ./run_all.sh delay
#
# Task sets must already exist (python3 generate_tasksets.py).
# The ranges and CCRs here must match PERIOD_RANGES and CCRS in common.py.
set -e
cd "$(dirname "$0")"

JOBS=${JOBS:-32}                   # parallel processes; override with JOBS=16 ./run_all.sh
                                   # keep it above 16, or the 16 hybrid runs (~12 h each) block everything queued behind them
RANGES="small medium large wide"
CCRS="0.1 0.4 1.0 2.0"
EXPERIMENTS=${@:-"hybrid delay skip naive basic"}   # slowest first, so the long hybrid runs start right away

for exp in $EXPERIMENTS; do
    for r in $RANGES; do
        if [ "$exp" = "basic" ]; then
            echo "python3 exp_basic.py $r"
        else
            for c in $CCRS; do
                echo "python3 exp_$exp.py $r $c"
            done
        fi
    done
done | xargs -P "$JOBS" -I{} sh -c '{}'
