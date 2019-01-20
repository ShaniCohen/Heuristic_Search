# https://github.com/ChristopherKing42/15puzzleSolver/blob/master/puzzle.py
import config as c
from bloom_filter_se import BloomFilter
from algo import Astar, speedy
from utils import eval_pos, display
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


def mainloop(conf):
    cols = ['puzzle_idx', 'algorithm', 'size_bloom_array', 'size_bloom_hash', 'size_bloom_all']
    results = pd.DataFrame(columns=cols)

    for puzzle in c.PUZZLES:
        # generate a bloom filter
        bloom = BloomFilter(max_elements=conf['max_elements'], error_rate=conf['error_rate'])
        # num_bits_bloom = bloom.num_bits_m

        # run A-star
        sol, count, count_seen, evaluated, closed_lst = run_Astar(puzzle=puzzle, epsilon=conf['epsilon'])
        # run Astar with bloom
        sol_b, count_b, count_seen_b, evaluated_b, bloom = run_Astar(puzzle=puzzle, epsilon=conf['epsilon'],
                                                                     bloom=bloom)
        # run speedy
        sol, count, count_seen, evaluated, closed_lst = run_speedy(puzzle=puzzle, epsilon=conf['epsilon'])
        # run speedy with bloom
        sol_b, count_b, count_seen_b, evaluated_b, bloom = run_speedy(puzzle=puzzle, epsilon=conf['epsilon'],
                                                                      bloom=bloom)

        print(f"count: {count}, count_seen: {count_seen}, evaluated: {evaluated}")
        print(f"count_b: {count_b}, count_seen_b: {count_seen_b}, evaluated_b: {evaluated_b}")
        # # compare memory size
        # size_bloom_array = sys.getsizeof(bloom)  # Return the size of an object in bytes
        # size_bloom_hash = sys.getsizeof(bloom.probe_bitnoer)
        # size_bloom_all = size_bloom_array + size_bloom_hash
        # closed_list_size = sys.getsizeof(closed_list)

        print(f"len of closed_list: {len(closed_lst)}")
        print('size of the close list: ', sys.getsizeof(closed_lst))
        print('size of the close bloom list (all): ', sys.getsizeof(bloom))
        # print('size of bloom (bits): ', bloom.num_bits_m)
        print('number of hash: ', bloom.num_probes_k)
        print('size of hash: ', sys.getsizeof(bloom.probe_bitnoer))


for configuration in c.CONFIGURATIONS:
    print(f"Configuration = {configuration['idx']}\n")
    # generate directory if not exist
    if not os.path.exists(join(c.output_path, 'conf_' + str(configuration['idx']))):
        os.makedirs(join(c.output_path, 'conf_' + str(configuration['idx'])))
    mainloop(conf=configuration)

