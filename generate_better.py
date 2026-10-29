import math
import random
# import arbitrary_deadline


def uunifast(n: int, U: float):
    utilizations = []
    total = U
    for i in range(1, n):
        next_total = total * (random.random() ** (1.0 / (n - i)))
        utilizations.append(total - next_total)
        total = next_total
    utilizations.append(total)
    return utilizations


def generate_taskset(n: int, U: float, T_min: int, T_max: int):
    utilizations = uunifast(n, U)
    tasks = []
    for u in utilizations:
        period = max(1, math.trunc(math.exp(random.uniform(math.log(T_min), math.log(T_max)))))
        cost = max(1, math.trunc(period * u))
        tasks.append((cost, period))
    return tasks
