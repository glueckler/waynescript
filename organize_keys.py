import os
import re
import shutil

import pprint
pp = pprint.PrettyPrinter(depth=4)
# pp.pprint(mydict)

keys_map = {
	"min": {
		# "a": [],
		# "b": [],
		# "c": [],
		# "d": [],
		# "e": [],
		# "f": [],
		# "g": []
	},
	"maj": {
		# "a": [],
		# "b": [],
		# "c": [],
		# "d": [],
		# "e": [],
		# "f": [],
		# "g": []
	}
}

dir_path = '/Users/code/Desktop/mock_samples'
	
# create the destination
dest_dir_path_root = os.path.join(dir_path, '..', 'waynesamples', 'keys')

try:
	shutil.rmtree(dest_dir_path_root)
except FileNotFoundError as e:
	pass

os.makedirs(dest_dir_path_root)

def analyze_dir(dir):
	for filename in os.listdir(dir):
		path = os.path.join(dir, filename)
		extension = os.path.splitext(filename)[1]

		if filename.startswith('.'): continue
		if os.path.isdir(path): 
			analyze_dir(path)
			continue

		# ignore if not audio file
		audio_extensions = ('wav', 'aiff', 'rx')
		if not extension.endswith(audio_extensions):
			continue

		# if we can't find a key in the sample name just skip it
		key_regex = re.compile(
			r'(^|[\s_])([abcdefg])[\s_]?((sharp|#)|(flat|b))?[\s_]?((min(or)?)|(maj(or)?))?([\s_]|$)(?!piano)', 
			re.IGNORECASE
			)

		key_search = key_regex.search(filename)
		if key_search: 
			key, sharp, flat, isminor, ismajor = key_search.group(2, 4, 5, 7, 9)
			# print(filename)
			# print(key)
			# print(isminor)
			# print(ismajor)
			if sharp:
				key = f'{key}#'
			elif flat:
				key = f'{key}b'

			if isminor:
				keys_map['min'].setdefault(key.lower(), []).append(path)
			else:
				keys_map['maj'].setdefault(key.lower(), []).append(path)


analyze_dir(dir_path)

for scale, keys in keys_map.items():
	folder_path = os.path.join(dest_dir_path_root, scale)
	# os.makedirs(folder_path) # don't think this is necessary if we can create both in next loop

	for key, paths in keys.items():
		key_folder_path = os.path.join(folder_path, key)
		os.makedirs(key_folder_path)

		for path in paths:
			shutil.copy(path, os.path.join(key_folder_path, os.path.split(path)[-1]))

print('done organizing keyed samples !')






















