from utils import moves, eval_pos
import random as rn


def is_in(pos, old, bloom, smart, conf):
    '''
    check if position was seen before
    '''
    if bloom:
        if smart:
            curr_elements = len(old)
            max_elements = conf["max_elements"]
            # probability to "listen" to the bloom
            if rn.randint(1, max_elements) < curr_elements:  # bloom is too full
                return False
            return str(pos) in bloom
        else:
            return str(pos) in bloom
    else:
        return pos in old


def Astar(conf, tree, old, epsilon, bloom=None, smart=False, count_seen=0, evaluated=1):
    # find best node in open list (minimal f = distance + heuristic)
    best_f = 1000000000  # Big number
    best_node = None
    for node in tree:
        if node[2] < best_f:
            best_f = node[2]
            best_node = node
    # remove best_node from open list
    tree.remove(best_node)

    # add best_node to closed list OR bloom
    if bloom:
        bloom.add(str(best_node[0]))
    old.add(best_node[0])

    # update board position
    new_poss = moves(position=best_node[0])
    # expand
    for (moved, pos) in new_poss:
        # Duplicates - when h is consistent, no node needs to be processed more than once
        if is_in(pos, old, bloom, smart, conf):
            count_seen += 1
            continue

        g = best_node[1] + 1
        f = eval_pos(board=pos, pathlength=g, e=epsilon)
        evaluated += 1
        tree.append((pos, g, f, best_node[3] + [moved]))
    return best_node, count_seen, evaluated


def speedy(conf, tree, old, epsilon, bloom=None, smart=False, count_seen=0, evaluated=1):
    # find best node in open list (minimal heuristic)
    best_h = 1000000000  # Big number
    best_g = 1000000000  # Big number
    best_node = None
    for node in tree:
        if node[2] < best_h or (node[2] == best_h and node[1] < best_g):
            best_h = node[2]
            best_g = node[1]
            best_node = node

    # remove best_node from open list
    tree.remove(best_node)

    # add best_node to closed list OR bloom
    if bloom:
        bloom.add(str(best_node[0]))
    old.add(best_node[0])

    # update board position
    new_poss = moves(position=best_node[0])
    # expand
    for (moved, pos) in new_poss:
        # Duplicates - when h is consistent, no node needs to be processed more than once
        if is_in(pos, old, bloom, smart, conf):
            count_seen += 1
            continue

        g = best_node[1] + 1
        h = eval_pos(board=pos, pathlength=0, e=epsilon)
        evaluated += 1
        tree.append((pos, g, h, best_node[3] + [moved]))
    return best_node, count_seen, evaluated

