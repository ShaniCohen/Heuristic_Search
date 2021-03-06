# https://github.com/ChristopherKing42/15puzzleSolver/blob/master/puzzle.py
import config as c
from bloom_filter_se import BloomFilter
from algo import Astar, speedy
from utils import eval_pos
import sys
import pandas as pd
from os.path import join
import numpy as np
import random as rn

# set random seeds
np.random.seed(c.SEED)
rn.seed(c.SEED)


def run_Astar(conf, puzzle, epsilon, bloom=None, smart=False):
    # start_tree = list of (pos, g, f, solution)
    start_tree = [(puzzle, 0, eval_pos(board=puzzle, pathlength=0, e=epsilon), [])]
    closed_list = set()

    # count - number of nodes inserted to closed list / bloom
    # count_seen - number of nodes "seen" in closed list / bloom --> nodes which were already visited
    best_node, count_seen, evaluated, close_size = Astar(conf=conf, tree=start_tree, old=closed_list, epsilon=epsilon, bloom=bloom,
                                             smart=smart)
    i=0
    while best_node[0] != c.WIN:
        # print(best_node)
        best_node, count_seen, evaluated, close_size = Astar(conf=conf, tree=start_tree, old=closed_list, epsilon=epsilon,
                                                 bloom=bloom, smart=smart, count_seen=count_seen, evaluated=evaluated)
        if best_node[0] =='-1':
            break
        if (smart and i>10000):
            best_node =('-1', '-1', '-1', '')
            break
        i+=1

    print('Solution:', '\n', best_node)
    if bloom:
        return best_node, count_seen, evaluated, bloom, close_size
    else:
        return best_node, count_seen, evaluated, closed_list, close_size


def run_speedy(conf, puzzle, epsilon, bloom=None, smart=False):
    # start_tree = list of (pos, g, h, solution)
    start_tree = [(puzzle, 0, eval_pos(board=puzzle, pathlength=0, e=epsilon), [])]
    closed_list = set()

    # count - number of nodes inserted to closed list / bloom
    # count_seen - number of nodes "seen" in closed list / bloom --> nodes which were already visited
    best_node, count_seen, evaluated, close_size = speedy(conf=conf, tree=start_tree, old=closed_list, epsilon=epsilon, bloom=bloom,
                                              smart=smart)
    i=0
    while best_node[0] != c.WIN:
        # print(best_node)
        best_node,  count_seen, evaluated, close_size = speedy(conf=conf, tree=start_tree, old=closed_list, epsilon=epsilon,
                                                   bloom=bloom, smart=smart, count_seen=count_seen, evaluated=evaluated)
        if best_node[0] =='-1':
            break
        if (smart and i>10000):
            best_node =('-1', '-1', '-1', '')
            break
        i+=1

    print('Solution:', '\n', best_node)
    if bloom:
        return best_node,  count_seen, evaluated, bloom, close_size
    else:
        return best_node,  count_seen, evaluated, closed_list, close_size


def update_results(results, puzzle_idx, algo, sol, sol_b, sol_sb, evaluated, evaluated_b, evaluated_sb, closed_lst,
                   bloom, s_bloom, count_seen, count_seen_b, count_seen_sb, close_size,close_size_b,close_size_sb):
    to_save = {'puzzle_idx': puzzle_idx,
               'algorithm': algo,
               'reg_sol_quality': len(sol[3]),  # solution quality
               'bloom_sol_quality': len(sol_b[3]),
               'smart_bloom_sol_quality': len(sol_sb[3]),
               'reg_evaluated': evaluated,  # run time
               'bloom_evaluated': evaluated_b,
               'smart_bloom_evaluated': evaluated_sb,
               'reg_count_seen': count_seen,  # FP indication
               'bloom_count_seen': count_seen_b,
               'smart_bloom_count_seen': count_seen_sb,
               'reg_closed_lst_size': sys.getsizeof(closed_lst),  # memory 1
               'reg_closed_lst_len': len(closed_lst),  # memory 2
               'bloom_array_size': sys.getsizeof(bloom),
               'bloom_hash_size': sys.getsizeof(bloom.probe_bitnoer),
               'bloom_size_all': sys.getsizeof(bloom) + sys.getsizeof(bloom.probe_bitnoer),
               'bloom_num_hash': bloom.num_probes_k,
               'smart_bloom_array_size': sys.getsizeof(s_bloom),
               'smart_bloom_hash_size': sys.getsizeof(s_bloom.probe_bitnoer),
               'smart_bloom_size_all': sys.getsizeof(s_bloom) + sys.getsizeof(s_bloom.probe_bitnoer),
               'smart_bloom_num_hash': s_bloom.num_probes_k,
               'close_size_list': close_size,
               'close_size_list_bloom': close_size_b,
               'close_size_list_smart_bloom': close_size_sb}
    #print(bloom.num_bits_m)
    results = results.append(to_save, ignore_index=True)
    # for k, v in to_save.items():
    #     print(f"{k}: {v}")
    print()
    return results


def mainloop(conf):
    i=1
    cols = ['puzzle_idx', 'algorithm', 'reg_sol_quality', 'bloom_sol_quality', 'smart_bloom_sol_quality',
            'reg_evaluated', 'bloom_evaluated', 'smart_bloom_evaluated',
            'reg_count_seen', 'bloom_count_seen', 'smart_bloom_count_seen',
            'reg_closed_lst_size', 'reg_closed_lst_len', 'bloom_array_size', 'bloom_hash_size', 'bloom_size_all',
            'bloom_num_hash', 'smart_bloom_array_size', 'smart_bloom_hash_size', 'smart_bloom_size_all', 'smart_bloom_num_hash']
    results = pd.DataFrame(columns=cols)
    for idx, puzzle in enumerate(c.PUZZLES):
        #####  A-star  #####
        print('A-star')
        sol, count_seen, evaluated, closed_lst, close_size = run_Astar(conf=conf, puzzle=puzzle, epsilon=conf['epsilon'])
        print('Astar with bloom')
        bloom = BloomFilter(max_elements=conf['max_elements']*close_size, error_rate=conf['error_rate'])
        sol_b, count_seen_b, evaluated_b, bloom, close_size_b = run_Astar(conf=conf, puzzle=puzzle, epsilon=conf['epsilon'],
                                                            bloom=bloom, smart=False)
        # print('Astar with smart bloom')
        # s_bloom = BloomFilter(max_elements=conf['max_elements'], error_rate=conf['error_rate'])
        # sol_sb, count_seen_sb, evaluated_sb, s_bloom, close_size_sb = run_Astar(conf=conf, puzzle=puzzle, epsilon=conf['epsilon'],
        #                                                          bloom=s_bloom, smart=False)
        results = update_results(results=results, puzzle_idx=idx, algo='Astar', sol=sol, sol_b=sol_b, sol_sb=sol_b,
                                 evaluated=evaluated, evaluated_b=evaluated_b, evaluated_sb=0,
                                 closed_lst=closed_lst, bloom=bloom, s_bloom=bloom,
                                 count_seen=count_seen, count_seen_b=count_seen_b, count_seen_sb=0,
                                 close_size=close_size,close_size_b=close_size_b,close_size_sb=0)
        #####  Speedy  #####
        print('Speedy')
        sol, count_seen, evaluated, closed_lst, close_size = run_speedy(conf=conf, puzzle=puzzle, epsilon=conf['epsilon'])
        print('Speedy with bloom')
        bloom = BloomFilter(max_elements=conf['max_elements']*close_size, error_rate=conf['error_rate'])
        sol_b, count_seen_b, evaluated_b, bloom, close_size_b = run_speedy(conf=conf, puzzle=puzzle, epsilon=conf['epsilon'],
                                                             bloom=bloom, smart=False)
        # print('Speedy with smart bloom')
        # s_bloom = BloomFilter(max_elements=conf['max_elements'], error_rate=conf['error_rate'])
        # sol_sb, count_seen_sb, evaluated_sb, s_bloom, close_size_sb = run_speedy(conf=conf, puzzle=puzzle, epsilon=conf['epsilon'],
        #                                                           bloom=s_bloom, smart=False)
        results = update_results(results=results, puzzle_idx=idx, algo='Speedy', sol=sol, sol_b=sol_b, sol_sb=sol_b,
                                 evaluated=evaluated, evaluated_b=evaluated_b, evaluated_sb=0,
                                 closed_lst=closed_lst, bloom=bloom, s_bloom=bloom,
                                 count_seen=count_seen, count_seen_b=count_seen_b, count_seen_sb=0,
                                 close_size=close_size,close_size_b=close_size_b,close_size_sb=0)
        print(i)
        i+=1

    results.to_csv(join(c.output_path, f"results_conf_{conf['idx']}.csv"), index=False)


for configuration in c.CONFIGURATIONS:
    print(f"Configuration = {configuration['idx']}\n")
    mainloop(conf=configuration)

