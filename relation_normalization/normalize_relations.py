import sys
import glob
import os
import random
import nltk


ann_dir = './annotated_json_cleaned/'
for file in os.listdir(ann_dir):
	with open(os.path.join(ann_dir, file), 'r') as f:
		print(f)