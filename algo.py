from utils import moves, eval_pos


def Astar(tree, old, epsilon, count_seen=0, count=0, count_seen_bloom=0, bloom=None):
    best_f = 1000000000  # Big number
    best_node = None
    for node in tree:
        if node[2] < best_f:
            best_f = node[2]
            best_node = node

    tree.remove(best_node)
    old.add(best_node[0])
    bloom.add(str(best_node[0]))
    count += 1
    # best_node is now the node with the best distance+heuristic
    new_poss = moves(position=best_node[0])
    for (moved, pos) in new_poss:
        # Duplicates
        if str(pos) in bloom:
            count_seen_bloom += 1
            continue
        if pos in old:  # I have seen this solution before
            count_seen += 1
            continue
        g = best_node[1] + 1
        f = eval_pos(board=pos, pathlength=g, e=epsilon)
        tree.append((pos, g, f, best_node[3] + [moved]))
    return best_node, count_seen, count, count_seen_bloom