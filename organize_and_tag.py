import os
import re
import shutil

from params import let_me_pick, default_pick


# dir_path = '/Users/code/Desktop/mock_samples'
# sample_type_regex = "kic?ks"
# sample_tag_str = 'randkicks'			
def organize(dir_path, dest_dir_path, sample_type_regex, sample_tag_str):

	# help add a tag to sample filenames
	def append_tag(filename):
	    name, ext = os.path.splitext(filename)
	    return "{name} --{sample_tag_str}{ext}".format(name=name, sample_tag_str=sample_tag_str, ext=ext)

	def analyse_sample_dir(dir, exact_match):
		samples_to_copy = []
		for filename in os.listdir(dir):
			# only count the first few..
			if len(samples_to_copy) > 25:
				break

			path = os.path.join(dir, filename)
			extension = os.path.splitext(filename)[1]

			# ignore hidden files
			if filename.startswith('.'):
				continue

			# dive into folder if it's a key
			key_regex = re.compile(
				r'^([abcdefg])[\s_]?((sharp|#)|(flat|b))?[\s_]?((min(or)?)|(maj(or)?))?$', 
				re.IGNORECASE
				)
			if key_regex.match(filename) and os.path.isdir(path):
				for sample_path in analyse_sample_dir(path, True):
					samples_to_copy.append(sample_path)

			# also dive into folders to find subfolders to analyze
			if os.path.isdir(path):
				print(f'diving deeper in directory {path}')
				analyse_dir(path)

			audio_extensions = ('wav', 'aiff', 'rx', 'mp3')
			if os.path.isfile(path) and extension.endswith(audio_extensions):
				samples_to_copy.append(os.path.join(dir, filename))

		if len(samples_to_copy) == 0:
			print(f"no sample files found in {dir}")
			return samples_to_copy

		copy_these_files = 'y'
		if not exact_match:
			print('found these files..')
			print('\n'.join(samples_to_copy))
			print('---')
			copy_these_files = default_pick
			if let_me_pick: copy_these_files = input("copy these files? (y means yes)")
			print('---')

		if copy_these_files == 'y':
			for source_filepath in samples_to_copy:
				destination_path = dest_dir_path 
				shutil.copy(
					source_filepath, 
					os.path.join(dest_dir_path, append_tag(os.path.split(source_filepath)[-1]))
					)
		return samples_to_copy

	def analyse_dir(dir):
		for filename in os.listdir(dir):
			path = os.path.join(dir, filename)

			# ignore all hidden files and non-directories
			if filename.startswith('.') or os.path.isfile(path):
				continue

			# ignore samples in any "loop" or "bpm" folder (look at parent directories)
			checked_loop_keywords = ('loop', 'bpm', 'roll')
			if any(x in path.lower() for x in checked_loop_keywords):
				continue

			exact_match = re.search(rf"^[^a-zA-Z]*({sample_type_regex})+[^a-zA-Z]*$", filename, flags=re.IGNORECASE)
			close_match = re.search(rf"({sample_type_regex})+([\s_\-](samples|hits|shots|sounds|tools|oneshots|one[\s_\-]shots))?_?$", filename, flags=re.IGNORECASE)
			match_in_string = re.search(rf"({sample_type_regex})+", filename, flags=re.IGNORECASE)

			if exact_match:
				print(f"Exact directory match on.. {exact_match.group(0)} <-- these should match --> {filename}\n{path}")
				analyse_sample_dir(path, True)
			elif close_match:
				print(f"---\nMatching: {sample_type_regex}\nClose Match {match_in_string.group(0)} <-- in directory --> {filename}\n{path}\n---")
				analyse_sample_dir(path, True)
			elif match_in_string:
				print(f"---\nMatching: {sample_type_regex}\nMatch in String: {match_in_string.group(0)} <-- in directory --> {filename}\n{path}\n---")
				analyse_sample_dir(path, False)
			else:
				analyse_dir(path)



	analyse_dir(dir_path)


