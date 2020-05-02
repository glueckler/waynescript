import os
import shutil

import organize_and_tag as organize

dir_path = '/Users/code/Desktop/mock_samples'

# example: ["REGEX", "TAG", "Destination Path"]
oneshot_types = [
	["kic?ks", "kkicks", "kkicks"],
	["snares", "ssnares", "ssnares"]
]

# create the destination
dest_dir_path_root = os.path.join(dir_path, '..', 'waynesamples', 'oneshots')
try:
	shutil.rmtree(dest_dir_path_root)
except FileNotFoundError as e:
	pass

os.makedirs(dest_dir_path_root)

# loop through all of the oneshot types
for oneshot_type in oneshot_types:
	sample_type_regex = oneshot_type[0]
	sample_tag_str = oneshot_type[1]

	dest_dir_path = os.path.join(dest_dir_path_root, oneshot_type[2])
	os.makedirs(dest_dir_path)

	organize.organize(dir_path, dest_dir_path, sample_type_regex, sample_tag_str)
