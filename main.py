# https://github.com/ChristopherKing42/15puzzleSolver/blob/master/puzzle.py
import config as c
from bloom_filter_se import BloomFilter
from algo import Astar
from utils import eval_pos, display
import sys
import os
from os.path import join


def mainloop(conf):
    for puzzle in c.PUZZLES:
        # generate a bloom filter
        bloom = BloomFilter(max_elements=conf['max_elements'], error_rate=conf['error_rate'],
                            array_size=conf['array_size'], hash_size=conf['hash_size'])
        start_0, start_1 = [(puzzle, 0, eval_pos(board=puzzle, pathlength=0, e=conf['epsilon']), [])], set()

        print(sys.getsizeof(start_1))
        print(sys.getsizeof(bloom))
        count_seen = 0
        # count- כמות קודקודים שמכניסים לרשימה הסגורה
        count = 0
        count_seen_bloom = 0
        x = 1000

        # run A-star
        best_node, _, count, count_seen_bloom = Astar(tree=start_0, old=start_1, epsilon=conf['epsilon'], count=count,
                                                      count_seen_bloom=count_seen_bloom, bloom=bloom)
        while best_node[0] != c.WIN:
            if x == 1000:
                display(best_node[0])
                print(best_node[1])
                x = 0
            # calling Astar
            best_node, count_seen, count, count_seen_bloom = Astar(tree=start_0, old=start_1, epsilon=conf['epsilon'],
                                                                   count=count, count_seen_bloom=count_seen_bloom,
                                                                   bloom=bloom)
            print(best_node)
            x += 1
        print(best_node)
        print(f"count: {count}, count_seen: {count_seen}, count_seen_bloom: {count_seen_bloom}")
        print('size of the close list: ', sys.getsizeof(start_1))
        print('size of the close bloom list: ', conf['array_size'])
        print('number of hash: ', bloom.num_probes_k)
        print('size of hash: ', sys.getsizeof(bloom.probe_bitnoer))


for configuration in c.CONFIGURATIONS:
    print(f"Configuration = {configuration['idx']}\n")
    # generate directory if not exist
    if not os.path.exists(join(c.output_path, 'conf_' + str(configuration['idx']))):
        os.makedirs(join(c.output_path, 'conf_' + str(configuration['idx'])))
    mainloop(conf=configuration)

