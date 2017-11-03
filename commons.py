# -*- coding: utf-8 -*-

#burden -> n # нагрузка
#bandage -> k # шина

import numpy
import collections

class RepresentationBasic(object):
    """
        Basic Representation of the current solution
    """
    
    def __init__(self, burdens, bandage_n, zero_assignments=False,
            burdens_assignmts=None, bandages_burdens=None, eval_repr=None):
        self.burdens = burdens
        self.bandage_n = bandage_n
        if burdens_assignmts is None:
            self.burdens_assignmts = self._burdens_init_zeroassignments(burdens, bandage_n) if zero_assignments \
                else self._burdens_init_rndassignments(burdens, bandage_n)
        else:
            self.burdens_assignmts = burdens_assignmts
        assert len(burdens) == len(self.burdens_assignmts)
        
        self.bandages_burdens_mem = bandages_burdens
#         self.bandages_burdens = self._get_updated_bandages_burdens() if bandages_burdens is None else bandages_burdens
        self._eval_mem = eval_repr
        
        self.duration = None
    
    def _burdens_init_zeroassignments(self, burdens, bandage_n):
        return [0]*len(burdens)
    
    def _burdens_init_rndassignments(self, burdens, bandage_n):
        return numpy.random.randint(bandage_n, size=len(burdens))
    
    def all_burdens_assigned(self):
        return all([a is not None for a in self.burdens_assignmts])
    
    def get_bandages_burdens(self):
        if self.bandages_burdens_mem is None:
            self.bandages_burdens_mem = self._get_updated_bandages_burdens()
        return self.bandages_burdens_mem
    
    def _get_updated_bandages_burdens(self):
        bandages_burdens = [0]*self.bandage_n
        for i in range(len(self.burdens)):
            if self.burdens_assignmts[i] is not None:
                bandages_burdens[self.burdens_assignmts[i]] += self.burdens[i]
        return bandages_burdens

    def eval_repr(self):
        if self._eval_mem is None:
            self._eval_mem = eval_repr(self.get_bandages_burdens())
        return self._eval_mem
    
    def get_bandage_assignmts(self):
        bandage_assignmts = collections.defaultdict(list)
        for i in range(len(self.burdens_assignmts)):
            bandage_assignmts[self.burdens_assignmts[i]].append(i)
        return bandage_assignmts
    
    def __str__(self):
        return "burdens={}\nbandage_n={}\nburdens_assignmts= {}\nbandage_assignmts= {}\nbandages_burdens= {}\neval: {}" \
            .format(self.burdens, self.bandage_n, self.burdens_assignmts,
                self.get_bandage_assignmts().items(), self.get_bandages_burdens(),
                self.eval_repr()) \
            + ("\nduration= {:.3f}s".format(self.duration) if self.duration is not None else "")

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False
     
    def __ne__(self, other):
        return not self.__eq__(other)
 
    def __hash__(self):
        return hash(frozenset(self.__dict__.iterkeys()))

def eval_repr(bandages_burdens):
    return numpy.std(bandages_burdens)
