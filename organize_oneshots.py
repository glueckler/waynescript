import os
import shutil

import organize_and_tag as organize
from params import source_path, dest_dir_name

dir_path = source_path

# example: ["REGEX", "TAG", "Destination Path"]
oneshot_types = [
	["(kic?k([_\s]?drum)?('?[sz])?)|(bass\s?drum('?[sz]))", "kkicks", "kkicks"],
	["snare(drum)?('?[sz])?([\s_\-](and|&)[\s_\-](rim|clap)('?[sz])?)?", "ssnares", "ssnares"],
	["[kc]lap('?[sz])", "cclaps", "cclaps"],
	["bass(?![\s_]?((guitar)|(drum)))", "bbass", "bbass"],
	["(?<!snare[\s_\-])808('?[sz])?([\s_\-]?bass)?", "eeight_oh_eight", "eeight_oh_eight"],
	["perc(ussion)?'?('?[sz])?", "pperc", "pperc"],
	["(ambience)|(ambient)|(atmos(phere)?)('?[sz])?", "aatmos", "aatmos"],
	["crash(es)?", "ccrash", "cymbols"],
	["ride('?[sz])?", "rride", "cymbols"],
	["cymbol('?[sz])?", "ccymbol", "cymbols"],
	["(open[_\s\-])?(hi[_\s\-]?)?(hat'?('?[sz])?)([_\-\s]open)?", "hhats", "hhats"],
	["tamb?", "ttam", "ttam"],
	["shaker'?('?[sz])", "sshaker", "sshakers"],
	["rim(shots)?('?[sz])?", "rrim", "rrim"],
	["((shout('?[sz])?)|(chant('?[sz])?)|(phrase('?[sz])?))([_\-\s]fx)?", "sshouts", "sshouts"],
	["vox", "vvox", "vvox"],
	["(roll(zs)?)|(fill'?('?[sz])?)", "ffills", "ffills"],
	["string('?[sz])?", "sstring", "sstring"],
	["buildup", "bbuildup", "bbuildup"],
	["conga('?[sz])?", "cconga", "cconga"],
	["(?<!cus)tom('?[sz])?", "ttom", "ttoms"],
	["foley", "ffoley", "ffoley"],
	["brass", "bbrass", "bbrass"],
	["snap('?[sz])?", "ssnaps", "ssnaps"],
	["break('?[sz])?", "bbreaks", "bbreaks"],
	["riser'?('?[sz])", "rrisers", "rrisers"],
	["noise", "nnoise", "nnoise"],
	["beat(box)?('?[sz])?", "bbeats", "bbeats"],
	["fx'?('?[sz])?", "ffxs", "ffxs"]
]

# create the destination
dest_dir_path_root = os.path.join(dir_path, '..', dest_dir_name, 'oneshots')
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
	if not os.path.exists(dest_dir_path):
		os.makedirs(dest_dir_path)

	organize.organize(dir_path, dest_dir_path, sample_type_regex, sample_tag_str)

	# if dir is empty delete it
	if len(os.listdir(dest_dir_path)) == 0:
  		shutil.rmtree(dest_dir_path)
