# -*- coding: utf-8 -*-

import time

import commons

def main():
#     print( "Result:\n{}".format(opt([10, 7], 2)) )
    print( "Result:\n{}".format(opt([5, 2, 3, 4], 3)) )
#     print( "Result:\n{}".format(opt([10, 7, 7, 5, 5, 4, 3, 2, 1, 1], 5)) )

def opt(burdens, bandage_n):
    start_time = time.time()
    
    opt_repr = commons.RepresentationBasic(burdens, bandage_n, zero_assignments=True)
    repr_next = None
    for burdens_assignmts in __gencompleteinclst(list(opt_repr.burdens_assignmts), bandage_n-1):
        if repr_next is None: # If it is the first iteration
            repr_next = opt_repr
            continue
        repr_next = commons.RepresentationBasic(burdens, bandage_n, burdens_assignmts=list(burdens_assignmts))
        if repr_next.eval_repr() < opt_repr.eval_repr():
            opt_repr = repr_next
    opt_repr.duration = time.time() - start_time
    return opt_repr

def __inclst(intlst, maxval):
    """
        intlst:list
            array representing a number (each item is a digit)
        maxval: int
            max. allowed value for each item in the list, intlst
    Returns
        intlst incremented by 1.
    """
    p=0
    n=len(intlst)
    while p<n:
        if intlst[p]+1 <= maxval:
            intlst[p]+=1
            return intlst
        else:
            intlst[p]=0
            p+=1
    else:
        return None


def __gencompleteinclst(intlst, maxval):
    """Get a generator, returning lists incremented by 1.
        List is considered as a number, each item is a digit of the number. 
    """
    i = intlst
    while i is not None:
        yield i
        i = __inclst(intlst, maxval)


if __name__ == '__main__':
    main()