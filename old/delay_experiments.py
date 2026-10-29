import math

import RTA

import generate_better

# import arbitrary_deadline

import random

import matplotlib.pyplot as plt

import numpy as np

import math

import sys





Inverted_TRADEOFFS = [0, 7, 12, 18, 21, 27, 29, 32, 33, 33, 34, 30, 31, 30]





inter_onions = np.load("inverted_pendulum_inter_onions.npy")

# Schecdat short: 3–33 ms, moderate: 10–100 ms, long: 50–250 ms



# def run_experiment_all(U_values , n , T_min, T_max, trials, check_cost_ratio, control_first):

#     TRADEOFFS=Inverted_TRADEOFFS

#     results_basic = []

#     results_naive = []

#     results_delay = []

#     results_skip = []

#     results_both = []

#     for U in U_values:

#         accepted_basic = 0

#         accepted_naive = 0

#         accepted_delay = 0

#         accepted_skip = 0  

#         accepted_both = 0 

#         print(f"**************** starting trials for util {U} *************")

#         for _ in range(trials):



#             ########## Generate Task Set ##############

#             ts = generate_better.generate_taskset(random.randint(1,n),U,T_min,T_max)

#             real_util = sum([ts[i][0]/ts[i][1] for i in range(len(ts))])



#             # print("utils", U, real_util)



#             # Make it rate monotonic

#             ts_rm = sorted(ts, key = lambda x: x[1])

#             # print("task set", ts)

#             # print()

#             # print("RM", ts_rm)

#             # make the task set a multi-frame task set

#             ts_multi = []

#             for t in ts_rm:

#                 ts_multi.append(([t[0]], t[1]))



#             # print("multiframe task set og", ts_multi)

#             # print(RTA.schedulable(ts_multi))



#             # ts_multi = []

#             # for t in ts_rm:

#             #     ts_multi.append(([t[0]], t[1]))



#             # print("multiframe task set rm", ts_multi)

#             # print(RTA.schedulable(ts_multi))





#             ########## Check if the normal task set is schedulable ##########

#             if RTA.schedulable(ts_multi):

#                 accepted_basic += 1

            

#             # assume that the first task is the control task

#             if control_first:

#                 control_idx = 0#random.randint(0, len(ts) -1)

#             else:

#                 control_idx = random.randint(0, len(ts) -1)



#             control_task = ts_multi[control_idx]

            

#             check_cost = math.ceil(control_task[0][0] * check_cost_ratio) # FIXME: make this realistic



#             # onion_level = random.randint(1, len(TRADEOFFS)-1)



#             ########### Check if it is schedulable with the naive security ###########

#             check_task_naive = ([check_cost], control_task[1])



#             ts_naive = ts_multi.copy()

#             ts_naive.insert(control_idx + 1, check_task_naive)



#             # print("naive taskset:",ts_naive)

#             # print(RTA.schedulable(ts_naive))



#             if RTA.schedulable(ts_naive):

#                 accepted_naive += 1



#             ########### Convert to an arbitrary deadline task set ##########

#             ts_delay = [(ts_multi[i][0],ts_multi[i][1], ts_multi[i][1]) for i in range(len(ts_multi))]

#             ts_delay.insert(control_idx + 1, (check_task_naive[0], check_task_naive[1], check_task_naive[1] + check_task_naive[1] * (len(TRADEOFFS) - 2)))



#             # print("delay taskset", ts_delay)



#             if RTA.ad_schedulable(ts_delay, ts_delay[control_idx], ts_delay[control_idx + 1]):

#                 accepted_delay += 1



#             ########## skip checks #######################

            

#             for y in range(1,len(TRADEOFFS)):



#                 check_task_skip = ([check_cost] * TRADEOFFS[y] + [0] * y , control_task[1])

#                 # check_task_skip =  ([0] * y  + [check_cost] * TRADEOFFS[y], control_task[1])

#                 ts_skip = ts_multi.copy()

#                 ts_skip.insert(control_idx + 1, check_task_skip)

#                 if RTA.schedulable(ts_skip):

#                     accepted_skip += 1

#                     break



#                 # print("skip task set", ts_skip)



#             # start in O(y)

#             # skip s checks

#             # delay checks for d itterations

#             # checks = #checks for O(y-s) -> O(y)

#             # requires

#             # d + s <= y

#             # d <= y - s

#             found = False

#             for y in range(1,len(TRADEOFFS)):

#                 # print(f"checking onion {y}")

#                 if found:

#                     break

#                 # r = TRADEOFFS[y]

#                 for d in range(y + 1):

#                     if found:

#                         break

#                     # print(f"trying delay {d}")

#                     for s in range(y - d + 1):

#                         if d == 0 and s == 0:

#                             continue

#                         # print("d", d, "s", s)

#                         # print("inter_onion" ,inter_onions[y - s, s])

#                         check_task_both = ([check_cost] + [check_cost] * (inter_onions[y, y - s] - 1) + [0] * s , control_task[1], control_task[1] + control_task[1] * d)

#                         # check_task_skip =  ([0] * y  + [check_cost] * TRADEOFFS[y], control_task[1])

#                         ts_both = [(ts_multi[i][0],ts_multi[i][1], ts_multi[i][1]) for i in range(len(ts_multi))]

#                         ts_both.insert(control_idx + 1, check_task_both)

#                         # print(ts_both)

#                         if RTA.ad_schedulable(ts_both, ts_both[control_idx], ts_both[control_idx + 1]):

#                             accepted_both += 1

#                             found = True

#                             break





#         results_basic.append((U, accepted_basic / trials))

#         results_naive.append((U, accepted_naive / trials))

#         results_delay.append((U, accepted_delay / trials))

#         results_skip.append((U, accepted_skip / trials))

#         results_both.append((U, accepted_both / trials))

#     return results_basic,results_naive,results_delay,results_skip,results_both







def run_experiment_delay(U_values , n , T_min, T_max, trials, check_cost_ratio, control_first):

    TRADEOFFS=Inverted_TRADEOFFS

    results_delay = []

    for U in U_values:

        # accepted_basic = 0

        # accepted_naive = 0

        accepted_delay = [0] * len(TRADEOFFS)

        # accepted_skip = 0  

        # accepted_both = 0 

        print(f"**************** starting trials for util {U} *************")

        for _ in range(trials):



            ########## Generate Task Set ##############

            ts = generate_better.generate_taskset(random.randint(1,n),U,T_min,T_max)

            real_util = sum([ts[i][0]/ts[i][1] for i in range(len(ts))])



            # print("utils", U, real_util)



            # Make it rate monotonic

            ts_rm = sorted(ts, key = lambda x: x[1])

            # print("task set", ts)

            # print()

            # print("RM", ts_rm)

            # make the task set a multi-frame task set

            ts_multi = []

            for t in ts_rm:

                ts_multi.append(([t[0]], t[1]))



            # print("multiframe task set og", ts_multi)

            # print(RTA.schedulable(ts_multi))



            # ts_multi = []

            # for t in ts_rm:

            #     ts_multi.append(([t[0]], t[1]))



            # print("multiframe task set rm", ts_multi)

            # print(RTA.schedulable(ts_multi))





            ########## Check if the normal task set is schedulable ##########

            # if RTA.schedulable(ts_multi):

            #     accepted_basic += 1

            

            # assume that the first task is the control task

            if control_first:

                control_idx = 0#random.randint(0, len(ts) -1)

            else:

                control_idx = random.randint(0, len(ts) -1)



            control_task = ts_multi[control_idx]

            

            check_cost = math.ceil(control_task[0][0] * check_cost_ratio) # FIXME: make this realistic



            # onion_level = random.randint(1, len(TRADEOFFS)-1)



            # ########### Check if it is schedulable with the naive security ###########

            check_task_naive = ([check_cost], control_task[1])



            # ts_naive = ts_multi.copy()

            # ts_naive.insert(control_idx + 1, check_task_naive)



            # # print("naive taskset:",ts_naive)

            # # print(RTA.schedulable(ts_naive))



            # if RTA.schedulable(ts_naive):

            #     accepted_naive += 1



            ########### Convert to an arbitrary deadline task set ##########



            for d in range(1, len(TRADEOFFS)):

                ts_delay = [(ts_multi[i][0],ts_multi[i][1], ts_multi[i][1]) for i in range(len(ts_multi))]

                ts_delay.insert(control_idx + 1, (check_task_naive[0], check_task_naive[1], check_task_naive[1] + check_task_naive[1] * (d - 1)))

                if RTA.ad_schedulable(ts_delay, ts_delay[control_idx], ts_delay[control_idx + 1]):

                    accepted_delay[d] += 1



            ########## skip checks #######################

            

            # for y in range(1,len(TRADEOFFS)):



            #     check_task_skip = ([check_cost] * TRADEOFFS[y] + [0] * y , control_task[1])

            #     # check_task_skip =  ([0] * y  + [check_cost] * TRADEOFFS[y], control_task[1])

            #     ts_skip = ts_multi.copy()

            #     ts_skip.insert(control_idx + 1, check_task_skip)

            #     if RTA.schedulable(ts_skip):

            #         accepted_skip += 1

            #         break



                # print("skip task set", ts_skip)



            # start in O(y)

            # skip s checks

            # delay checks for d itterations

            # checks = #checks for O(y-s) -> O(y)

            # requires

            # d + s <= y

            # d <= y - s

            # found = False

            # for y in range(1,len(TRADEOFFS)):

            #     # print(f"checking onion {y}")

            #     if found:

            #         break

            #     # r = TRADEOFFS[y]

            #     for d in range(y + 1):

            #         if found:

            #             break

            #         # print(f"trying delay {d}")

            #         for s in range(y - d + 1):

            #             if d == 0 and s == 0:

            #                 continue

            #             # print("d", d, "s", s)

            #             # print("inter_onion" ,inter_onions[y - s, s])

            #             check_task_both = ([check_cost] + [check_cost] * (inter_onions[y, y - s] - 1) + [0] * s , control_task[1], control_task[1] + control_task[1] * d)

            #             # check_task_skip =  ([0] * y  + [check_cost] * TRADEOFFS[y], control_task[1])

            #             ts_both = [(ts_multi[i][0],ts_multi[i][1], ts_multi[i][1]) for i in range(len(ts_multi))]

            #             ts_both.insert(control_idx + 1, check_task_both)

            #             # print(ts_both)

            #             if RTA.ad_schedulable(ts_both, ts_both[control_idx], ts_both[control_idx + 1]):

            #                 accepted_both += 1

            #                 found = True

            #                 break

        u_results = []

        for i in range(len(accepted_delay)):

            u_results.append(accepted_delay[i] / trials)

        results_delay.append((U, u_results))

    return results_delay











if __name__ == "__main__":



    bounds = [(3000,30000),(10000, 100000), (50000, 250000), (3000,250000)]

    control_first = [True]

    check_cost_ratio = [.1, 0.4, 1.0, 2.0]



    # for i in range(len(inter_onions)):

    #     for j in range(len(inter_onions[0])):

    #         inter_onions[i][j] = int(inter_onions[i][j]/5.0)



    # print(inter_onions)



    # for control in control_first:

    #     for lb, ub in bounds:

    #         for check_cost in check_cost_ratio:



    lb = int(sys.argv[1])

    ub = int(sys.argv[2])

    check_cost = float(sys.argv[3])

    control = True



    results_delay = run_experiment_delay([.1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0], 20, 10000, 100000, 1000, 2.0, False)

    # results_basic, results_naive, results_delay, results_skip, results_both = run_experiment_all([.1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0], 20, lb, ub, 100, check_cost, control)



    # for results, label in [

    #     (results_basic, "Basic"),

    #     (results_naive, "Naive security"),

    #     (results_delay, "Delay (arbitrary deadline)"),

    #     (results_skip,  "Skip"),

    #     (results_both, "Skip & Delay"),

    # ]:

    #     U_vals, rates = zip(*results)

    #     plt.plot(U_vals, rates, marker="o", label=label)



    # plt.xlabel("Utilization")

    # plt.ylabel("Schedulable fraction")

    # plt.legend()

    # plt.tight_layout()

    # plt.savefig(f"results_all/schedulability_curves_{lb}_{ub}_{check_cost}_{control}.png", dpi=150)

    # plt.show()

    # plt.close()



    # for i in range(1, len(Inverted_TRADEOFFS)):

    #     plt.plot([.1, .2], results_delay[::,i])



    # for results, label, linestyle, alpha in [

    #     (results_delay, "Delay (arbitrary deadline)", "-.", 0.75),

    # ]:

    #     U_vals, rates = zip(*results)



    #     plt.plot(

    #         U_vals,

    #         rates,

    #         marker="o",

    #         linestyle=linestyle,

    #         linewidth=2.2,

    #         alpha=alpha,

    #         label=label,

    #     )



    results = results_delay

    utilizations = [u for u, values in results]



    # # Number of indices in the second dimension

    num_indices = len(results[0][1])



    plt.figure(figsize=(10, 6))



    # One line per index in the second dimension

    for i in range(1, num_indices):

        y_values = [values[i] for u, values in results]

        plt.plot(utilizations, y_values, marker="o", label=f"Delayed {i} iterations")



    plt.xlabel("Utilization")

    plt.ylabel("Schedulability")

    plt.title("Schedulability vs Utilization by Delay Amount")

    plt.ylim(-0.05, 1.05)

    plt.grid(True)



    # plt.legend(

    #     title="Second-dimension index",

    #     bbox_to_anchor=(1.05, 1),

    #     loc="upper left"

    # )



    plt.tight_layout()

    # plt.show()



    # plt.xlabel("Utilization")

    # plt.ylabel("Schedulable fraction")

    plt.legend()

    plt.tight_layout()

    plt.savefig(f"results_delay/schedulability_curves_{10000}_{100000}_{2.0}_{False}.pdf", dpi=150)

    # plt.show()

    # plt.close()