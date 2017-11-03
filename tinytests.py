# -*- coding: utf-8 -*-

import myheuristics


def main():
    burdens = [1000, 1000, 50, 50]
    bandage_n = 2
    feval(burdens, bandage_n, 1)
    
    burdens = [1000, 50, 50]
    bandage_n = 2
    feval(burdens, bandage_n, 2)
    
    burdens = [1000, 50, 1000, 50]
    bandage_n = 2
    feval(burdens, bandage_n, 3)
    
    burdens = [1]*50
    bandage_n = 6
    feval(burdens, bandage_n, 4)
    

def feval(burdens, bandage_n, test_num):
    print( "\n== Test {} ==".format(test_num) )
    mh = myheuristics.MyHeuristics(burdens, bandage_n,
        10, # max_tries
        len(burdens)^2 * bandage_n^2, # max_iter. Rough estimation
        10, # tabu_max_n
        10, # tabu_max_iter
        permutation_ratio = 0.5,
        max_t_s = 4,
        initialisation_approach = myheuristics.INITIALISATION_APPROACH_RND)
    res = mh.opt()
    print( "Result:\n{}".format(res) )
    print(mh)
    
if __name__ == '__main__':
    main()
