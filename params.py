import os

env_source_path = os.environ['SRC_PATH']
source_path = env_source_path
print(f'Path to samples is.. {source_path}')
dest_dir_name = os.path.join(source_path, '../waynesamples')

let_me_pick = False
default_pick = 'y'
