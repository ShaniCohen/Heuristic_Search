# https://github.com/ChristopherKing42/15puzzleSolver/blob/master/puzzle.py
import config as c
from bloom_filter_se import BloomFilter
from algo import Astar, speedy
from utils import eval_pos
import sys
import os
import pandas as pd
from os.path import join


def run_Astar(puzzle, epsilon, bloom=None):
    # start_tree = list of (pos, g, f, solution)
    start_tree = [(puzzle, 0, eval_pos(board=puzzle, pathlength=0, e=epsilon), [])]
    closed_list = set()

    # count - number of nodes inserted to closed list / bloom
    # count_seen - number of nodes "seen" in closed list / bloom --> nodes which were already visited
    best_node, count, count_seen, evaluated = Astar(tree=start_tree, old=closed_list, epsilon=epsilon, bloom=bloom)
    while best_node[0] != c.WIN:
        print(best_node)
        best_node, count, count_seen, evaluated = Astar(tree=start_tree, old=closed_list, epsilon=epsilon, bloom=bloom,
                                                        count=count, count_seen=count_seen, evaluated=evaluated)
    print('Solution:', '\n', best_node)
    if bloom:
        return best_node, count, count_seen, evaluated, bloom
    else:
        return best_node, count, count_seen, evaluated, closed_list


def run_speedy(puzzle, epsilon, bloom=None):
    # start_tree = list of (pos, g, h, solution)
    start_tree = [(puzzle, 0, eval_pos(board=puzzle, pathlength=0, e=epsilon), [])]
    closed_list = set()

    # count - number of nodes inserted to closed list / bloom
    # count_seen - number of nodes "seen" in closed list / bloom --> nodes which were already visited
    best_node, count, count_seen, evaluated = speedy(tree=start_tree, old=closed_list, epsilon=epsilon, bloom=bloom)
    while best_node[0] != c.WIN:
        print(best_node)
        best_node, count, count_seen, evaluated = speedy(tree=start_tree, old=closed_list, epsilon=epsilon, bloom=bloom,
                                                         count=count, count_seen=count_seen, evaluated=evaluated)
    print('Solution:', '\n', best_node)
    if bloom:
        return best_node, count, count_seen, evaluated, bloom
    else:
        return best_node, count, count_seen, evaluated, closed_list


def update_results(results, puzzle_idx, algo, sol, sol_b, evaluated, evaluated_b, closed_lst, bloom):
    to_save = {'puzzle_idx': puzzle_idx,
               'algorithm': algo,
               'reg_sol_quality': len(sol[3]),  # solution quality
               'bloom_sol_quality': len(sol_b[3]),
               'reg_evaluated': evaluated,  # run time
               'bloom_evaluated': evaluated_b,
               'reg_closed_lst_size': sys.getsizeof(closed_lst),  # memory 1
               'reg_closed_lst_len': len(closed_lst),  # memory 2
               'bloom_array_size': sys.getsizeof(bloom),
               'bloom_hash_size': sys.getsizeof(bloom.probe_bitnoer),
               'bloom_size_all': sys.getsizeof(bloom) + sys.getsizeof(bloom.probe_bitnoer),
               'num_hash': bloom.num_probes_k}
               # bloom.num_bits_m
    results = results.append(to_save, ignore_index=True)
    for k, v in to_save.items():
        print(f"{k}: {v}")
    print()
    return results


def mainloop(conf):
    results = pd.DataFrame()
    for idx, puzzle in enumerate(c.PUZZLES):
        #####  A-star  #####
        bloom = BloomFilter(max_elements=conf['max_elements'], error_rate=conf['error_rate'])
        # run A-star
        sol, count, count_seen, evaluated, closed_lst = run_Astar(puzzle=puzzle, epsilon=conf['epsilon'])
        # run Astar with bloom
        sol_b, count_b, count_seen_b, evaluated_b, bloom = run_Astar(puzzle=puzzle, epsilon=conf['epsilon'],
                                                                     bloom=bloom)
        results = update_results(results=results, puzzle_idx=idx, algo='Astar', sol=sol, sol_b=sol_b,
                                 evaluated=evaluated, evaluated_b=evaluated_b, closed_lst=closed_lst, bloom=bloom)
        #####  Speedy  #####
        bloom = BloomFilter(max_elements=conf['max_elements'], error_rate=conf['error_rate'])
        # run speedy
        sol, count, count_seen, evaluated, closed_lst = run_speedy(puzzle=puzzle, epsilon=conf['epsilon'])
        # run speedy with bloom
        sol_b, count_b, count_seen_b, evaluated_b, bloom = run_speedy(puzzle=puzzle, epsilon=conf['epsilon'],
                                                                      bloom=bloom)
        results = update_results(results=results, puzzle_idx=idx, algo='Speedy', sol=sol, sol_b=sol_b,
                                 evaluated=evaluated, evaluated_b=evaluated_b, closed_lst=closed_lst, bloom=bloom)
    results.to_csv(join(c.output_path, f"results_conf_{conf['idx']}.csv"), index=False)


for configuration in c.CONFIGURATIONS:
    print(f"Configuration = {configuration['idx']}\n")
    mainloop(conf=configuration)

