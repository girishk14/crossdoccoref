import sys
import glob
import os
import random
import nltk
import json

ann_dir = './annotated_json_cleaned/'
stanford_coref_dir = './pos_matched/'

for file in os.listdir(ann_dir):

	if not file.endswith(".json"):
		continue

	with open(os.path.join(ann_dir, file), 'r') as f:
		ann_json = json.load(f)

		for chain_id in ann_json['corefs']:
			chain =  ann_json['corefs'][chain_id]
			for mention in chain:
				del mention['animacy']
				del mention['isRepresentativeMention']
				del mention['gender']
				del mention['id']
				del mention['number']
				del mention['position']
				sent_num, start_idx, end_idx = mention['sentNum'],mention['startIndex'], mention['endIndex']
				del mention['sentNum']
				del mention['startIndex']
				del mention['endIndex']

				mention['pos'] = []

				for idx in range(start_idx -1 , end_idx - 1):
					mention['pos'].append(ann_json['sentences'][sent_num -1]['tokens'][idx]['pos'])

				print(mention)
				sys.exit()