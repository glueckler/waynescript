import sys

if len(sys.argv) < 2:
	raise ValueError('Not enough command line parameters')

samples_dir = sys.argv[1]
print(f"Script working on directory {samples_dir}")

