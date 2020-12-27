import argparse
import base64
import json
import os
import os.path as osp

import imgviz
import PIL.Image

from labelme.logger import logger
from labelme import utils


def main():
	logger.warning(
		"This script is aimed to demonstrate how to convert the "
		"JSON file to a single image dataset."
	)
	logger.warning(
		"It won't handle multiple JSON files to generate a "
		"real-use dataset."
	)

	parser = argparse.ArgumentParser()
	# parser.add_argument("json_file")
	parser.add_argument("-i", "--input", required=True,
				help="path to json files")
	parser.add_argument("-o", "--out", default=None)
	args = vars(parser.parse_args())

	path_to_json = args['input']
	json_file = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')] 
	
	for i in range(0,len(json_file)):
		print(json_file[i])
		
		if args["out"] is None:
			out_dir = osp.basename(json_file[i]).replace(".", "_")
			out_dir = osp.join(osp.dirname(json_file[i]), out_dir)
		else:
			out_dir = args["out"]
		if not osp.exists(out_dir):
			os.mkdir(out_dir)

		data = json.load(open(json_file[i]))
		imageData = data.get("imageData")
		is_labeled = data.get("shapes")
		

		if not imageData:
			imagePath = os.path.join(os.path.dirname(json_file[i]), data["imagePath"])
			with open(imagePath, "rb") as f:
				imageData = f.read()
				imageData = base64.b64encode(imageData).decode("utf-8")
		img = utils.img_b64_to_arr(imageData)

		label_name_to_value = {"_background_": 0}
		for shape in sorted(data["shapes"], key=lambda x: x["label"]):
			label_name = shape["label"]
			if label_name in label_name_to_value:
				label_value = label_name_to_value[label_name]
			else:
				label_value = len(label_name_to_value)
				label_name_to_value[label_name] = label_value
		# lbl, _ = utils.shapes_to_label(
		# 	img.shape, data["shapes"], label_name_to_value
		# )

		label_names = [None] * (max(label_name_to_value.values()) + 1)
		for name, value in label_name_to_value.items():
			label_names[value] = name

		# lbl_viz = imgviz.label2rgb(
		# 	label=lbl, img=imgviz.asgray(img), label_names=label_names, loc="rb"
		# )
		if is_labeled != []:
			PIL.Image.fromarray(img).save(osp.join(out_dir, f"{json_file[i]}.bmp"))
		else:
			os.remove(json_file[i])
		
		logger.info("Saved to: {}".format(out_dir))


if __name__ == "__main__":
	main()
