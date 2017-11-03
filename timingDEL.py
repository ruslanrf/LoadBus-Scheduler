"""
Times the execution of various parts of the tool.

Used for our evaluation.
"""

import time
import collections



class Timing:
    def __init__(self):
        # Maps names to lists of durations.
        self._finished_timers = collections.defaultdict(list)
        # Maps names to the start times.
        self._running_timers = {}
    
    def start_timer(self, name):
        assert(name not in self._running_timers)
        self._running_timers[name] = time.time()
    
    def stop_timer(self, name):
        assert(name in self._running_timers)
        stop_time = time.time()
        start_time = self._running_timers[name]
        del self._running_timers[name]
        self._finished_timers[name].append(stop_time-start_time)
    
    def elapsed_time(self, name):
        if name in self._running_timers:
            return [time.time()-self._running_timers[name]]
        elif name in self._finished_timers:
            return self._finished_timers[name]
        else:
            raise Exception("Unknown name of a timer")
    
    def stats(self):
        assert(len(self._running_timers) == 0)
        
        result = "\n"
        for name, all_times in self._finished_timers.items():
            assert(len(all_times) > 0)
            if len(all_times) > 1:
                for idx, duration in enumerate(all_times, 1):
                    result += "Timing::{}[{}]: {:.3f}s\n".format(name, idx, duration)
            else:
                result += "Timing::{}: {:.3f}s\n".format(name, all_times[0])
        return result
    
    def get_aggregated_stats(self):
        rez = {}
        for name, all_times in self._finished_timers.items():
            assert(len(all_times) > 0)
            rez[name] = reduce(lambda x, y: x+y, all_times)
        return rez
    

TimeLog = Timing()

class TimeThis:
    """A context manager for timing a code snippet."""
    def __init__(self, name, timer=TimeLog):
        self._name = name
        self._timer = timer
    def __enter__(self):
        self._timer.start_timer(self._name)
    def __exit__(self, type, value, traceback):
        self._timer.stop_timer(self._name)





