import os
import re
import shutil
import librosa

from params import source_path, dest_dir_name

import pprint
pp = pprint.PrettyPrinter(depth=4)
# pp.pprint(mydict)

loops_dictionary = {}

dir_path = source_path
# create the destination
dest_dir_path_root = os.path.join(dir_path, '..', dest_dir_name, 'loops')

try:
	shutil.rmtree(dest_dir_path_root)
except FileNotFoundError as e:
	pass

os.makedirs(dest_dir_path_root)

def analyze_dir(dir):
	# do stuff
	copy_these_files = True
	for filename in os.listdir(dir):
		path = os.path.join(dir, filename)
		extension = os.path.splitext(filename)[1]

		# ignore directories and hidden files
		if filename.startswith('.'):
			continue

		if os.path.isdir(path):
			copy_these_files = True
			analyze_dir(path)
			continue

		# ignore if not audio file
		audio_extensions = ('wav', 'aiff', 'rx')
		if not extension.endswith(audio_extensions):
			continue

		# if we can't find a number that represents the bpm, just skip it
		# so check for a number first
		bpm_numeric_regex_str = "[6-9][0-9]|1[0-8][0-9]"
		bpm_regex_without_bpm = re.compile(rf"[\s_]({bpm_numeric_regex_str})[\s_]")

		bpm_match = bpm_regex_without_bpm.search(filename)

		# skip if no matching bpm
		if not bpm_match: continue

		# some keywords to check for, if these are found in the filename ask about skipping the directory..
		# checked_keywords = ('impact', '808')
		# if any(x in filename.lower() for x in checked_keywords):
		# 	pp.pprint(list(filter(bpm_regex_without_bpm.search, os.listdir(dir))))
		# 	print(f'FILE IN QUESTION: {filename}')
		# 	print(f'FROM DIRECTORY: {dir}')
		# 	copy_these_files = input("copy these files? (y means yes)")
		# 	if copy_these_files != 'y': break


		# check if the "bpm" is included in filename
		word_bpm_in_filename = "bpm" in filename.lower()

		if not word_bpm_in_filename:
			# ignore if file is short audio file (ie oneshot)
			audio_len = 0
			try:
				audio_len = int(librosa.get_duration(filename=path))
			except Exception as e:
				print(e.__doc__)
				print(getattr(e, 'message', 'no message available for error'))
				print(f'ERROR GETTING DURATION OF FILE: {filename}')	

			if audio_len < 4:
				continue

			word_loops_in_filename = "loops" in path.lower()

			bpm = bpm_match.group(1)

			pp.pprint(list(filter(bpm_regex_without_bpm.search, os.listdir(dir))))
			print(f'FILE IN QUESTION: {filename}')
			print(f'FROM DIRECTORY: {dir}')
			print(f'at bpm: {bpm}')
			if copy_these_files == True: copy_these_files = input("copy these files? (y means yes)")
			if copy_these_files != 'y': break

			bpm = bpm_match.group(1)
			paths_at_bpm = loops_dictionary.setdefault(bpm, [])
			paths_at_bpm.append(path)

		else:  # in this case, the word bpm is in the filename
			bpm_regex_with_bpm = re.compile(rf"(^|[\s_])((bpm[\s_]?)({bpm_numeric_regex_str})|({bpm_numeric_regex_str})([\s_]?bpm))([\s_]?|$)", re.IGNORECASE)
			bpm_match = bpm_regex_with_bpm.search(filename)
			if not bpm_match: print(f'REGEX: {str(bpm_regex_with_bpm)} for filename didnt match For FILENAME: {filename}')
			bpm = bpm_match.group(4) or bpm_match.group(5)
			paths_at_bpm = loops_dictionary.setdefault(bpm, [])
			paths_at_bpm.append(path)
			
			


analyze_dir(dir_path)
if not loops_dictionary: 
	print ("\n\nno loops found!!\n\n")

organized_loops_dict = {}
lowest_bpm = min(map(lambda x: int(x), loops_dictionary.keys())) # map(lambda x: x + x, numbers)
highest_bpm = max(map(lambda x: int(x), loops_dictionary.keys()))
max_loops_per_bpm = len(loops_dictionary) / 20

bpm_range = range(lowest_bpm, highest_bpm)
low_bpm_of_group = str(lowest_bpm)
high_bpm_of_group = str(lowest_bpm)
group_of_loops = []

pp.pprint(loops_dictionary)

for bpm in bpm_range:
	bpm = str(bpm)
	is_last_bpm_of_group = False
	if bpm == high_bpm_of_group: is_last_bpm_of_group = True

	if not bpm in loops_dictionary: continue

	nxt_bpm = str(int(bpm) + 1)
	while not nxt_bpm in loops_dictionary and not is_last_bpm_of_group:
		nxt_bpm = str(int(nxt_bpm) + 1)

	if not group_of_loops:
		low_bpm_of_group = bpm
		high_bpm_of_group = bpm

	if low_bpm_of_group == bpm:
		group_of_loops = loops_dictionary[low_bpm_of_group]

	# print("bpm current: " + bpm)
	# print("nxt_bpm: " + nxt_bpm)
	# print(len(group_of_loops))

	if len(group_of_loops) + len(loops_dictionary.get(nxt_bpm, [])) > max_loops_per_bpm:
		name_of_group_key = f"{low_bpm_of_group}-{high_bpm_of_group}"
		if low_bpm_of_group == high_bpm_of_group:
			name_of_group_key = low_bpm_of_group

		organized_loops_dict[name_of_group_key] = group_of_loops

		low_bpm_of_group = bpm
		high_bpm_of_group = bpm
		group_of_loops = []
		continue

	group_of_loops += loops_dictionary[bpm]
	high_bpm_of_group = bpm

# pp.pprint(organized_loops_dict)

for folder, paths in organized_loops_dict.items():
	folder_path = os.path.join(dest_dir_path_root, folder)
	os.makedirs(folder_path)
	for path in paths:
		shutil.copy(
					path, 
					os.path.join(folder_path, os.path.split(path)[-1])
					)

print('done with flying colors !')


























