import argparse
from collections import Counter
import json
import os
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
				help="path to json files")
ap.add_argument("-n", "--name", required=True,
				help="name of dataset creator")
args = vars(ap.parse_args())



nomask_couner = 0
unclear_counter = 0
mask_counter = 0
wrong_counter = 0
path_to_json = args['input']
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')] 
print(len(json_files))
for i in range(0,len(json_files)):
	print(json_files[i])
	try:
		print(i)
		with open(path_to_json+json_files[i], "r") as read_file:
			data = json.load(read_file)
		
			for key, value in data.items():
				if key == 'shapes':
					for i in range(len(value)):
						if value[i]['label'] == 'nomask':
							nomask_couner+=1
						elif value[i]['label'] == 'unclear':
							unclear_counter+=1
						elif value[i]['label'] == 'mask':
							mask_counter+=1
						elif value[i]['label'] == 'wrong':
							wrong_counter+=1
						print(value[i]['label'])	
	except:
		pass
	
print("nomask:",nomask_couner)
print("unclear:",unclear_counter)
print("mask:",mask_counter)
print("wrong:",wrong_counter)
all_data = ["nomask:"+str(nomask_couner)+"\n", "unclear:"+str(unclear_counter)+"\n", "mask:"+str(mask_counter)+"\n","wrong:"+str(wrong_counter)+"\n"]
with open(args['name']+".txt", 'w') as write_file:
	write_file.writelines(all_data)