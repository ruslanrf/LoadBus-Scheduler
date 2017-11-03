# -*- coding: utf-8 -*-

import mymetaheuristics
import lpt

import random, numpy#, collections

INITIALISATION_APPROACH_LPT = "lpt"
INITIALISATION_APPROACH_RND = "rnd"
INITIALISATION_APPROACH_0 = "0"
INITIALISATION_APPROACH_INITASSIGN = "burdens_init_assignmts"


class MyHeuristics(mymetaheuristics.MyMetaHeuristics):
    def __init__(self, burdens, bandage_n, max_tries, max_iter, tabu_max_n, tabu_max_iter,
        burdens_init_assignmts = None, permutation_ratio=1,
        max_t_s=None,
        initialisation_approach = INITIALISATION_APPROACH_RND):
        super(MyHeuristics, self).__init__(burdens, bandage_n, max_tries,
            max_iter, tabu_max_n, tabu_max_iter,
            burdens_init_assignmts = burdens_init_assignmts,
            permutation_ratio=permutation_ratio, max_t_s=max_t_s)
        self.initialisation_approach = initialisation_approach
        
        self.neigh_search_mode = 0
        self.neigh_search_processed_bandages = set()

        
    def _generate_init_solution(self, rep=None, permutation_ratio=1):
        if rep is None:
            if self.initialisation_approach == INITIALISATION_APPROACH_INITASSIGN:
                if self.burdens_init_assignmts is None:
                    raise Exception("Initial burden assignments hasn't been provided")
                else:
                    return mymetaheuristics.Representation(self.burdens,
                        self.bandage_n, burdens_assignmts=self.burdens_init_assignmts)
            # Apply LPT approach
            if self.initialisation_approach == INITIALISATION_APPROACH_LPT:
                oldrepr = lpt.opt(self.burdens, self.bandage_n)
                return mymetaheuristics.Representation(oldrepr.burdens, oldrepr.bandage_n,
                    burdens_assignmts=oldrepr.burdens_assignmts)
            # Random assignments
            elif self.initialisation_approach == INITIALISATION_APPROACH_RND:
                return mymetaheuristics.Representation(self.burdens,
                   self.bandage_n, zero_assignments=False)
            # assign bandage 0 to all burdens
            elif self.initialisation_approach == INITIALISATION_APPROACH_RND:
                return mymetaheuristics.Representation(self.burdens,
                   self.bandage_n, zero_assignments=True)
            else:
                raise Exception("Initialisation strategy for the initial solution is unknown")
        else: # make a permutations
            burdens_idxs = list(range(len(self.burdens)))
            random.shuffle(burdens_idxs)
            burdens_assignmts_src = numpy.random.randint(self.bandage_n, size=len(self.burdens))
            i=0
            burdens_assignmts = list(rep.burdens_assignmts)
            while i < permutation_ratio*len(self.burdens):
                burdens_assignmts[burdens_idxs[i]] = burdens_assignmts_src[i]
                i += 1
            return mymetaheuristics.Representation(self.burdens, self.bandage_n,
                burdens_assignmts=burdens_assignmts)
    
    def _get_neighbourhood(self, rep, is_new_settings=False):
        """
            It finds the better solutions.
            Result is a list of representations (solutions) with transformations
        """
        if is_new_settings:
            self.neigh_search_mode = 0
            self.neigh_search_processed_bandages = set()
        
        if len(self.neigh_search_processed_bandages) == self.bandage_n:
            return []
        
        bandages_burdens = rep.get_bandages_burdens()
        bb_ens = sorted(enumerate(bandages_burdens), key=lambda k: k[1], reverse=True)
        bandage_assignmts = rep.get_bandage_assignmts()
        
        transformations = []
        # Current mode is to move one burden
        if self.neigh_search_mode == 0:
            # iterate over sorted enumerated list of bandages_burdens
            for bb_en in bb_ens:
                # if this bandage hasn't been processed
                if bb_en[0] not in self.neigh_search_processed_bandages:
                    if bb_en[0] not in bandage_assignmts:
                        continue
                    # do not optimise the recent largest bandage with a single burden
                    if len(bandage_assignmts[bb_en[0]]) == 1:
                        continue
                    min_burden_idx = min(bandage_assignmts[bb_en[0]],
                        key=lambda b: self.burdens[b])
                    for band_idx in range(self.bandage_n):
                        if band_idx != bb_en[0] \
                            and bandages_burdens[band_idx]<bb_en[1]- 2*self.burdens[min_burden_idx]:
                            transformations.append(frozenset([(min_burden_idx, band_idx)]))
                    # transformation for the current bandage has been found
                    if len(transformations) > 0:
                        return [rep.instantiate_neighbour(tr) for tr in transformations]
                    else:
                        self.neigh_search_processed_bandages.add(bb_en[0])
            # No neighbours, we change the mode
            self.neigh_search_mode = 1
            self.neigh_search_processed_bandages = set()
        
        # Current mode is to move one burden
        if self.neigh_search_mode == 1:
            global_min_burden = min(self.burdens)
            # iterate over sorted enumerated list of bandages_burdens
            for bb_en in bb_ens:
                # if this bandage hasn't been processed
                if bb_en[0] not in self.neigh_search_processed_bandages:
                    if bb_en[0] not in bandage_assignmts:
                        continue
                    # do not optimise the recent largest bandage with a single burden
                    if len(bandage_assignmts[bb_en[0]]) == 1:
                        continue
                    # sort burdens of the current bandage in ascending order by their value
                    curr_str_burden_idxs = sorted(bandage_assignmts[bb_en[0]],
                        key=lambda b: self.burdens[b], reverse=True)
                    if self.burdens[curr_str_burden_idxs[0]] == global_min_burden :
                        break
                    # iterate over sorted burden indexes
                    burden_idx_prev = None
                    for burden_idx in curr_str_burden_idxs:
                        if burden_idx_prev is not None \
                            and self.burdens[burden_idx] == self.burdens[burden_idx_prev]:
                            continue
                        # iterate over bandage indexes
                        for band_idx2 in range(self.bandage_n):
                            if band_idx2 != bb_en[0] \
                                and bandages_burdens[band_idx2]<bb_en[1]:
                                curr_str_burden_idxs2 = sorted(bandage_assignmts.get(band_idx2, []),
                                    key=lambda b: self.burdens[b], reverse=True)
                                # iterate over sorted burden indexes
                                for burden_idx2 in curr_str_burden_idxs2:
                                    if self.burdens[burden_idx2] < self.burdens[burden_idx]:
                                        if self.burdens[burden_idx]-self.burdens[burden_idx2] \
                                                < bb_en[1] - bandages_burdens[band_idx2]:
                                            transformations.append(frozenset([(burden_idx, band_idx2),
                                                                    (burden_idx2, bb_en[0])]))
                                        break
                        # transformation for the current bandage has been found
                        if len(transformations) > 0:
                            return [rep.instantiate_neighbour(tr) for tr in transformations]
                        burden_idx_prev = burden_idx
                    assert len(transformations) == 0
                    self.neigh_search_processed_bandages.add(bb_en[0])
        
        assert len(transformations) == 0
        return []
        