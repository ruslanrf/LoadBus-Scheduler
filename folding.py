# -*- coding: utf-8 -*-

import time, sys

import commons

def main():
#     print( "Result:\n{}".format(opt([10, 7], 2)) )
#     print( "Result:\n{}".format(opt([5, 2, 3, 4], 3)) )
    print( "Result:\n{}".format(opt([10, 7, 7, 5, 5, 4, 3, 2, 1, 1], 5)) )

def opt(burdens, bandage_n):
    start_time = time.time()
    
    burdens_n = len(burdens)
    c = burdens_n/bandage_n
    if c%2 == 1:
        c -=1
    burdens_assignmts = [None]*len(burdens)
    
    for i in range(bandage_n):
        for j in range(1, c+1):
            if j==1:
                burdens_assignmts[i] = i
            elif j%2==0:
                burdens_assignmts[ j*bandage_n - i -1 ] = i
            else:
                burdens_assignmts[ (j-1)*bandage_n + i ] = i
        
    # enumerate burdens to remember their original positions/idexes
    # Sort all burdens such that burdens[i] >= burdens[i+1]
    eburdens = sorted(enumerate(burdens), key=lambda k: k[1], reverse=True)
    
    burdens_assignmts2 = [None]*len(burdens)
    for i in range(len(burdens_assignmts)):
        burdens_assignmts2[eburdens[i][0]] = burdens_assignmts[i]
    
    print burdens_assignmts
    print burdens_assignmts2
    print eburdens
    print burdens
    
    rep = commons.RepresentationBasic(burdens, bandage_n, burdens_assignmts=burdens_assignmts2)
    if not rep.all_burdens_assigned():
        sys.stderr.write("Not all burdens are assigned")
    
    rep.duration = time.time() - start_time
    return rep

if __name__ == '__main__':
    main()