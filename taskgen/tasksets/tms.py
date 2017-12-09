import random
from taskgen.taskset import TaskSet

"""
class WaitingTask(PeriodicTask):
    # priority
    # 
    pass

class MkGenerator(TaskSet):

    def __init__(size, t_min, t_max, k_min, k_max, u_t, d_u, g_c):
        super().__init__()

        # execution time weight
        weights = [random.randint(1, g_c) for s in size]
        weights_sum = sum(weights)
        
        for w in weights:
            # m, k
            period = random.randint(t_min, t_max) # period
            k = random.randint(k_min, k_max)
            m = random.randint(1, k)
            
            # execution time
            u = random.randint(u_t - max(u_t, d_u), u_t + d_u) # u = u_t ± d_u
            execution_time = max(1, round((u/w)*period*w))
            # todo remove ts with an utilisation outside of u.

            task = WaitingTask()
            task['id'] = 'id_{}'.format(w)
            task['period'] = period
            task['offset'] = 0 # hardcoded in mktask.cpp
            task['priority'] = 128 # TODO

            task['config']['duration'] = execution_time

"""
