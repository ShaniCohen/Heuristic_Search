from os.path import join, sep
from os import getcwd

if 'ssarusi' in getcwd():
    git_path = join('C:', sep, 'Users', 'ssarusi', 'git')
elif 'add_yours' in getcwd():
    git_path = 'add_yours'

data_path = join(git_path, 'Knowledge_graph', 'Imported_data')