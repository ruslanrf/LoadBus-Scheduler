# -*- coding: utf-8 -*-

import commons

import time

def main():
#     print( "Result:\n{}".format(opt([10, 7], 2)) )
#     print( "Result:\n{}".format(opt([5, 2, 3, 4], 3)) )
    print( "Result:\n{}".format(opt([10, 7, 7, 5, 5, 4, 3, 2, 1, 1], 5)) )

def opt(burdens, bandage_n):
    start_time = time.time()
    
    # enumerate burdens to remember their original positions/idexes
    eburdens = list(enumerate(burdens))
    # Sort all burdens such that burdens[i] >= burdens[i+1]
    eburdens = sorted(eburdens, key=lambda k: k[1], reverse=True)
    burdens_assignmts = [None]*len(burdens)
    bandages_burdens = [0]*bandage_n
    _bandage_ids = range(bandage_n)
    for i in range(len(eburdens)):
        j = min(_bandage_ids, key=lambda k: bandages_burdens[k])
        burdens_assignmts[eburdens[i][0]] = j
        bandages_burdens[j] += eburdens[i][1]
    
    rep = commons.RepresentationBasic(burdens, bandage_n, burdens_assignmts=burdens_assignmts, bandages_burdens=bandages_burdens)
    rep.duration = time.time() - start_time
    return rep

if __name__ == '__main__':
    main()