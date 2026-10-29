import math
from fractions import Fraction
import numpy as np

def ceil(a, b):
    return -(-a // b)

def interference(task, start, end):
    if start > start + end - 1:
        return 0
    n = len(task[0]) # number of frames
    total_interference = 0
    for l in range(start, start + end):
        total_interference += task[0][l % n]

    return total_interference

def _response_time(task, r, higher_priority):
    Cm = task[0][0]  # assuming AM ordering of frames (i.e. C_0 == C_m)
    hp_interference = 0
    for tj in higher_priority:
        hp_interference += interference(tj, 0, ceil(r, tj[1]))

    return Cm + hp_interference # assumming no blocking from lower priority tasks

def response_time(task, higher_priority):
    D = task[1] # assuming implicit deadlines
    r = task[0][0] # initial condition for the recurrance relation
    while True:
        r_next = _response_time(task, r, higher_priority)
        # print("ri =", r_next)
        if r_next > D:
            return None
        if r_next == r:
            return r
        r = r_next

def schedulable (taskset):
    for i in range(len(taskset)):
        if response_time(taskset[i], taskset[:i]) is None:
            return False
    
    return True


#############################################################


def r(q, task, higher_priority):
    r = interference(task, 0, q)
    while True:
        # print("r =", r)
        hp_interference = 0
        for tj in higher_priority:
            hp_interference += interference(tj, 0, ceil(r, tj[1]))

        r_next = interference(task, 0, q) + hp_interference

        if r_next == r:
            return r
        
        r = r_next

def w(q, task, higher_priority):
    ri = r(q, task, higher_priority)
    return ri - ((q - 1) * task[1]) # ri(q) − (q − 1)Ti

def ad_response_time(task, higher_priority):
    # asume task is ([C0, C1, ...], T, D) where D >= T
    C, T, D = task[0][0], task[1], task[2]
    U_i = Fraction(C, T) + sum([Fraction(math.ceil(sum(x[0]) / len(x[0])), x[1]) for x in higher_priority], Fraction(0))
    if U_i >= 1:
        return None
    sumC = C + sum(x[0][0] for x in higher_priority)
    q_max = ceil(sumC, (1 - U_i) * T)

    # print(q_max)


    Ri = 0
    q = 1
    Ti = task[1]
    while True:
        # print("q =", q)
        wq = w(q, task, higher_priority)
        if wq > Ri:
            Ri = wq
            if Ri > D:
                return None
        if wq <= Ti:
            return Ri
        q += 1
        assert q <= q_max, f"q {q} exceeded bound {q_max}; utilization guard failed"


def ad_schedulable(taskset, check_task, control_task):
    # # check utilization first
    # U = sum([Fraction(sum(x[0]) / len(x[0]), x[1]) for x in taskset], Fraction(0))
    U = sum([Fraction(math.ceil(sum(x[0]) / len(x[0])), x[1]) for x in taskset], Fraction(0))
    # U = sum([Fraction(sum([x[0] / len(x[0], x[1]) for x in taskset]], Fraction(0))
    if U >= 1:
        # print("ad taskset failed utilization test")
        return False


    # U = sum([taskset[i][0][0]/ taskset[i][1] for i in range(len(taskset))])
    # if U >= 1:
    #     print("util test failed")
    #     return False
    
    not_scheduled = taskset.copy()
    not_scheduled = [x for x in not_scheduled if x is not control_task]
    not_scheduled.reverse()
    check_scheduled = False
    while len(not_scheduled) > 0:
        # print("top of while loop")
        found = False
        for t in not_scheduled:
            # print("top of for loop")
            # build higher_priority
            hp = [x for x in not_scheduled if x is not t]
            if not check_scheduled:
                hp.append(control_task)
            Ri = ad_response_time(t, hp)
            if Ri is None:
                continue
            elif Ri <= t[2]:
                # print("found one")
                if t is check_task:
                    not_scheduled.append(control_task)
                    check_scheduled = True
                not_scheduled.remove(t)
                found = True
                break
        if not found:
            return False
    
    return True





#############################################

# Build task set
# task is ([C0, C1, C2, ...], T)

# t0 = ([1],4, 4)
# t1 = ([2], 6, 6)
# t2 = ([4], 10, 12)

# taskset = [t0, t1, t2]

# print(ad_response_time(t2, [t0, t1]))
# # print(response_time(t0, []))

# print(ad_schedulable(taskset))