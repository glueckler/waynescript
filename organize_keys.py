import os
import re
import shutil

from params import source_path, dest_dir_name

import pprint
pp = pprint.PrettyPrinter(depth=4)
# pp.pprint(mydict)

keys_map = {}

dir_path = source_path
	
# create the destination
dest_dir_path_root = os.path.join(dir_path, '..', dest_dir_name, 'keys')
try:
	shutil.rmtree(dest_dir_path_root)
except FileNotFoundError as e:
	pass

os.makedirs(dest_dir_path_root)

def analyze_dir(dir):
	for filename in os.listdir(dir):
		path = os.path.join(dir, filename)
		extension = os.path.splitext(filename)[1]
		filename_nopath = os.path.splitext(filename)[0]

		if filename.startswith('.'): continue
		if os.path.isdir(path): 
			analyze_dir(path)
			continue

		# ignore if not audio file
		audio_extensions = ('wav', 'aiff', 'rx', 'mp3')
		if not extension.endswith(audio_extensions):
			continue

		# if we can't find a key in the sample name just skip it
		key_regex = re.compile(
			r'(^|[\s_\-])([abcdefg])[\s_\-]?((sharp|#)|(flat|b))?[\s_]?((m(in(or)?)?)|(maj(or)?))?([\s_]|$)(?!piano)', 
			re.IGNORECASE
			)

		key_search = key_regex.search(filename_nopath)
		if key_search: 
			key, sharp, flat, isminor, ismajor = key_search.group(2, 4, 5, 7, 10)

			if isminor:
				keys_map.setdefault(f"{key.lower()}{('#' if sharp else '')}{'b' if flat else ''}_min", []).append(path)
			elif ismajor:
				keys_map.setdefault(f"{key.lower()}{('#' if sharp else '')}{'b' if flat else ''}_maj", []).append(path)
			else:
				# attempt to get smarter on the regex
				key_after_bpm = re.search(
					rf"([6-9][0-9]|1[0-8][0-9])[\s_\-]?(bpm)?[_\-\s]([abcdefg])[\s_\-]?((sharp|#)|(flat|b))?[\s_]?((m(in(or)?)?)|(maj(or)?))?([\.\s_\-]|$)", 
					filename_nopath, 
					re.IGNORECASE
					)
				if key_after_bpm: 
					key, sharp, flat, isminor, ismajor = key_after_bpm.group(3, 5, 6, 8, 11)
					if isminor:
						keys_map.setdefault(f"{key.lower()}{('#' if sharp else '')}{'b' if flat else ''}_min", []).append(path)
					else:
						keys_map.setdefault(f"{key.lower()}{('#' if sharp else '')}{'b' if flat else ''}_maj", []).append(path)
					continue

				multiple_possible = re.findall(rf"(^|[\s_\-])([abcdefg])([\s_\-]|$)", filename_nopath, re.IGNORECASE)
				if len(multiple_possible) == 1:
					keys_map.setdefault(f"{multiple_possible[0][1].lower()}_maj", []).append(path)
				elif len(multiple_possible) > 1:
					print("MORE THEN ONE KEY MATCH FOUND!!")
					print(f'FILE IN QUESTION: {path}')
					print(f'FILENAME: {filename}')
					print(list(map(lambda x: x[1], multiple_possible)))
					key_input = input("press enter button to skip or, enter key: ")
					if re.search(r"[a-g]", key_input): 
						keys_map.setdefault(f"{key_input.lower()}_maj", []).append(path)


analyze_dir(dir_path)

for key, paths in keys_map.items():
	key_folder_path = os.path.join(dest_dir_path_root, key)
	os.makedirs(key_folder_path)
	for path in paths:
		shutil.copy(path, os.path.join(key_folder_path, os.path.split(path)[-1]))


print('done organizing keyed samples !')






















