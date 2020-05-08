import os
import re

keywords = {}

dir_path = '/Users/code/Desktop/mock_samples'
reggy = '[a-zA-Z]+'

def analyse_dir(dir):
	for filename in os.listdir(dir):
		if filename.startswith('.'):
			continue

		path = os.path.join(dir, filename)


		
		if not os.path.isdir(path): continue

		analyse_dir(path)

		words_in_filename = re.findall(reggy, filename.lower())
		for word in words_in_filename:
			if word in keywords:
				keywords[word] = keywords[word] + 1
			else:
				keywords[word] = 1

analyse_dir(dir_path)

# sort that keywords bitch..
sorted_keywords = {k: v for k, v in sorted(keywords.items(), key=lambda item: item[1], reverse=True)}

for k, v in sorted_keywords.items():
	print(f'{k} x {v}')
