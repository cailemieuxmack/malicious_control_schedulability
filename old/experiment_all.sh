#! /bin/bash

bounds=(
    "3000 30000"
    "10000 100000"
    "50000 250000"
    "3000 250000"
)


check_cost_ratio=(
    "0.1"
    "0.4"
    "1.0"
    "2.0"
)

for bound in "${bounds[@]}"; do
    read -r lower_bound upper_bound <<< "$bound"
        for ratio in "${check_cost_ratio[@]}"; do
            python3 delay_experiments.py $lower_bound $upper_bound $ratio &
        done
done