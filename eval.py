# -*- coding: utf-8 -*-

from random import randint

import brute_force, lpt, folding, myheuristics

def main_large_eval():
    
    bandage_n = 6;
    burden_n = 50;
    min_burden = 1;
    max_burden = 100;
    
    print("== Large Evaluation ==\nbandage_n= {}\nburden_n= {}\nmin_burden= {}\nmax_burden= {} "
          .format(bandage_n, burden_n, min_burden, max_burden))
    
    lpt_data = []
    mh_data = []
    
    for i in range(100):
        print("\n=== Evaluation {} ===\n".format(i+1))
        
        burdens = gen_seed(burden_n, min_burden, max_burden)
        
        print("\n-- LPT --")
        lpt_res = lpt.opt(burdens, bandage_n)
        lpt_data.append(lpt_res)
        print("--- Results ---\n{}".format(lpt_res))
    
        print("\n-- MyHeuristics --")
        mh = myheuristics.MyHeuristics(burdens, bandage_n,
            1000, # max_tries
            len(burdens)^2 * bandage_n^2, # max_iter. Rough estimation
            100, # tabu_max_n
            100, # tabu_max_iter
            permutation_ratio = 0.5,
            max_t_s = 4,
            initialisation_approach = myheuristics.INITIALISATION_APPROACH_RND)
        mh_res = mh.opt()
        mh_data.append((mh, mh_res))
        print("--- Results ---")
        print("---- Solution ----\n{}".format(mh_res))
        print("---- Approach ----\n{}".format(mh))
    
    # average eval for LPT
    lpt_eval_mean = sum([v.eval_repr() for v in lpt_data])/len(lpt_data)
    # average duration for LPT
    lpt_duration_mean = sum([v.duration for v in lpt_data])/len(lpt_data)
    
    # average eval for MH to find the best solution
    mh_eval_mean = sum([v[1].eval_repr() for v in mh_data])/len(mh_data)
    # average duration for MH to find the best solution
    mh_duration_mean = sum([v[1].duration for v in mh_data])/len(mh_data)
    # average tries for MH to find the best solution
    mh_tries_mean = sum([v[1].tries_n for v in mh_data])/len(mh_data)
    # average iterations for MH
    mh_iter_mean = sum([v[1].iter_n for v in mh_data])/len(mh_data)
    # average duration for MH
    mh_duration_mean_all = sum([v[0].duration_all for v in mh_data])/len(mh_data)
    # average tries for MH
    mh_tries_mean_all = sum([v[0].tries_all for v in mh_data])/len(mh_data)
    # average iterations for MH
    mh_iter_mean_all = sum([v[0].iter_all for v in mh_data])/len(mh_data)
    
    print ("=== Statistics ===")
    print ("lpt_eval_mean= {}".format(lpt_eval_mean))
    print ("lpt_duration_mean= {}".format(lpt_duration_mean))
    print ("mh_eval_mean= {}".format(mh_eval_mean))
    print ("mh_duration_mean= {}".format(mh_duration_mean))
    print ("mh_tries_mean= {}".format(mh_tries_mean))
    print ("mh_iter_mean= {}".format(mh_iter_mean))
    print ("mh_duration_mean_all= {}".format(mh_duration_mean_all))
    print ("mh_tries_mean_all= {}".format(mh_tries_mean_all))
    print ("mh_iter_mean_all= {}".format(mh_iter_mean_all))
    

def basic_tests():
#     #1
#     burdens = [4, 3, 2, 1, 1, 7, 10, 5, 5, 7]
#     bandage_n = 5
#     burdens_init_assignmts = [0,0,0,0,0,1,2,3,3,4]
    
#     #2
#     burdens = [5, 4, 4, 2]
#     bandage_n = 2
#     burdens_init_assignmts = [0,0,1,1]

#     #3
#     burdens = gen_seed(50, 0, 100)
    burdens = gen_seed(50, 0, 100)
    bandage_n = 5
    burdens_init_assignmts = None
    
    res = lpt.opt(burdens, bandage_n)
    print( "== LPT Result:\n{}".format(res) )
    
    res = folding.opt(burdens, bandage_n)
    print( "== Folding Result:\n{}".format(res) )
    
    mh = myheuristics.MyHeuristics(burdens, bandage_n,
        1000, # max_tries
        len(burdens)^2 * bandage_n^2, # max_iter. Rough estimation
        100, # tabu_max_n
        100, # tabu_max_iter
        burdens_init_assignmts = burdens_init_assignmts,
        permutation_ratio = 0.5,
        max_t_s = 4,
        initialisation_approach = myheuristics.INITIALISATION_APPROACH_RND)
    res = mh.opt()
    print( "== MYHEURISTICS Result:\n{}".format(res) )
    print(mh)
    
#     res = brute_force.opt(burdens, bandage_n)
#     print( "== Brute Force Result:\n{}".format(res) )

def gen_seed(burden_n, burden_min, burden_max):
    assert burden_min <= burden_max
    burdens = [None]*burden_n
    for i in range(len(burdens)):
        burdens[i] = randint(burden_min, burden_max)
    return burdens
    
if __name__ == '__main__':
    main_large_eval()
#     basic_tests()