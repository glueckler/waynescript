import os
import re
import shutil


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
			# only count the first 10
			if len(samples_to_copy) > 9:
				break

			path = os.path.join(dir, filename)

			# ignore directories and hidden files
			if filename.startswith('.') or os.path.isdir(path):
				continue

			samples_to_copy.append(os.path.join(dir, filename))

		copy_these_files = 'y'
		if not exact_match:
			print('\n'.join(samples_to_copy))
			copy_these_files = input("copy these files? (y means yes)")

		if copy_these_files == 'y':
			for source_filepath in samples_to_copy:
				destination_path = dest_dir_path 
				shutil.copy(
					source_filepath, 
					os.path.join(dest_dir_path, append_tag(os.path.split(source_filepath)[-1]))
					)

	def analyse_dir(dir):
		for filename in os.listdir(dir):
			path = os.path.join(dir, filename)

			# ignore all hidden files and non-directories
			if filename.startswith('.') or os.path.isfile(path):
				continue

			exact_match = re.search(rf"^{sample_type_regex}$", filename, flags=re.IGNORECASE)
			match_in_string = re.search(rf"\b{sample_type_regex}\b", filename, flags=re.IGNORECASE)

			if exact_match:
				analyse_sample_dir(path, True)
			elif match_in_string:
				print(f"FROM DIRECTORY: {path}")
				analyse_sample_dir(path, False)
			else:
				analyse_dir(path)



	analyse_dir(dir_path)


