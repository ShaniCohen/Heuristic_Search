import conf_list as cl
import puzzles as p
from os.path import join, sep
from os import getcwd

if 'ssarusi' in getcwd():
    git_path = join('C:', sep, 'Users', 'ssarusi', 'git')
elif 'add_yours' in getcwd():
    git_path = 'add_yours'

output_path = join(git_path, 'Heuristic_Search', 'outputs_hs')

# region Params

WIN = ((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15, None))
PUZZLES = p.puzzles_to_solve
# CONFIGURATIONS = cl.configurations
CONFIGURATIONS = cl.configurations_to_run
SEED = 10

# endregion
