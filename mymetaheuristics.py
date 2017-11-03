# -*- coding: utf-8 -*-

import collections

import commons, time

class Representation(commons.RepresentationBasic):
    def __init__(self, burdens, bandage_n, zero_assignments=False,
                burdens_assignmts=None, bandages_burdens=None, eval_repr=None,
                transformation = None):
        super(Representation, self).__init__(
            burdens, bandage_n, zero_assignments=zero_assignments,
            burdens_assignmts=burdens_assignmts, bandages_burdens=bandages_burdens,
            eval_repr = eval_repr)
        self.transformation = transformation
        
        self.tries_n = None
        self.iter_n = None
        self.duration = None
        
    def instantiate_neighbour(self, transformation):
        burdens_assignmts = list(self.burdens_assignmts)
        bandages_burdens = list(self.get_bandages_burdens())
        for assign in transformation:
            bandages_burdens[ burdens_assignmts[assign[0]] ] -= self.burdens[assign[0]]
            bandages_burdens[assign[1]] += self.burdens[assign[0]]
            burdens_assignmts[assign[0]] = assign[1]
        rep = Representation(self.burdens, self.bandage_n,
                burdens_assignmts=burdens_assignmts,
                bandages_burdens=bandages_burdens,
            transformation=transformation)
        return rep
    
    def __str__(self):
        s = super(Representation, self).__str__()
        return s \
            + ("\ntries_n= {};".format(self.tries_n) if self.tries_n is not None else "") \
            + ("iter_n= {};".format(self.iter_n) if self.iter_n is not None else "")  
    
class MyMetaHeuristics(object):
    
    def __init__(self, burdens, bandage_n, max_tries, max_iter, tabu_max_n,
            tabu_max_iter, burdens_init_assignmts = None, permutation_ratio=1,
            max_t_s=None):
        self.burdens = burdens
        self.bandage_n = bandage_n
        self.burdens_init_assignmts = burdens_init_assignmts
        
        self.max_tries = max_tries
        self.max_iter = max_iter
        
        self.tabu_max_n = tabu_max_n
        self.tabu_max_iter = tabu_max_iter
        self._reset_memoisation()
        
        self.permutation_ratio = permutation_ratio
        self.max_t_s = max_t_s
        
        self.tries_all = None
        self.iter_all = None
        self.duration_all = None
    
    def _reset_memoisation(self):
        self.tabu = {} # key: set([(burden_value, bandage_id)...]), value: number of iterations
        self.frequency = {} # key: set([(burden_value, bandage_id)...]), value: number of use
#         self.improvements = {} # key: set([(burden_value, bandage_id)...]), value: number of iterations
    
    def opt(self):
        start_time = time.time()
        
        hot_exit = False
        local_best_solution, global_best_solution = None, None
        iter_all = 0
        for tries in range(self.max_tries):
            is_new_settings = True
            self._reset_memoisation()
            # generate initial solution
            local_best_solution = self._generate_init_solution(rep=local_best_solution, permutation_ratio=self.permutation_ratio)
            if tries == 0:
                global_best_solution = local_best_solution
            for _ in range(self.max_iter):
                iter_all += 1
                neighbours = self._get_neighbourhood(local_best_solution, is_new_settings=is_new_settings)
                best_neigh = self._select_best_neighbour_tabu(neighbours, local_best_solution, global_best_solution)
                time_elapsed = time.time() - start_time
                if self.max_t_s is not None and time_elapsed >= self.max_t_s:
                    hot_exit = True
                if best_neigh is not None:
                    self._add_info_mem(best_neigh.transformation)
                    local_best_solution = best_neigh
                    local_best_solution.tries_n = tries
                    local_best_solution.iter_n = iter_all
                    local_best_solution.duration = time_elapsed
                else:
                    break
                if hot_exit:
                    break
                is_new_settings = False
            if local_best_solution.eval_repr() < global_best_solution.eval_repr():
                global_best_solution = local_best_solution
            if hot_exit:
                break
        
        self.duration_all = time.time() - start_time
        self.tries_all = tries
        self.iter_all = iter_all
        
        return global_best_solution
    
    def __str__(self):
        return "" \
            + ("duration_all= {:.3f}s;".format(self.duration_all) if self.duration_all is not None else "") \
            + ("\ntries_all= {};".format(self.tries_all) if self.tries_all is not None else "") \
            + ("iter_all= {};".format(self.iter_all) if self.iter_all is not None else "")
    
    def _generate_init_solution(self, rep=None, permutation_ratio=1):
        pass
    
    def _get_neighbourhood(self, rep, is_new_settings=False):
        """
            It finds the better solutions.
            Result is a list of representations (solutions) with transformations
        """
        pass
    
    def _select_best_neighbour_tabu(self, neighbours, local_best_solution, global_best_solution):
        if len(neighbours) == 0:
            return None
        neigh_evalgrs = collections.defaultdict(list)
        for neighbour in neighbours:
            neigh_evalgrs[neighbour.eval_repr()].append(neighbour)
        srt_evals = sorted( list(set(map(lambda n: n.eval_repr(), neighbours))) )
        for eval_repr in srt_evals:
            if eval_repr < local_best_solution.eval_repr():
                neighs_orig = neigh_evalgrs[eval_repr]
                neighs = [n for n in neighs_orig if n.transformation not in self.tabu]
                # aspiration criterion
                if len(neighs) == 0 and eval_repr < global_best_solution.eval_repr():
                    neighs = neighs_orig
                if len(neighs) > 0:
                    # diversification of search
                    neighs = sorted(neighs, key=lambda n: self.frequency.get(n.transformation, 0))
                    return neighs[0]
            else:
                return None
        return None
    
    def _add_info_mem(self, transformation):
        self.__add_into_tabu(transformation)
        self.__add_into_freq(transformation)
    
    def __add_into_tabu(self, transformation):
        for key in self.tabu.keys():
            self.tabu[key] -= 1
        self.tabu[transformation] = self.tabu_max_iter
        if len(self.tabu) > self.tabu_max_n:
            item = min(self.tabu.items(), key=lambda i: i[1])
            del self.tabu[item[0]]
            assert len(self.tabu) == self.tabu_max_n
    
    def __add_into_freq(self, transformation):
        if transformation in self.frequency:
            self.frequency[transformation] += 1
        else:
            self.frequency[transformation] = 1
        if len(self.frequency) > self.tabu_max_n:
            item = max(self.frequency.items(), key=lambda i: i[1])
            del self.frequency[item[0]]
            assert len(self.frequency) == self.tabu_max_n
