import sys
import glob
import os
import random
import nltk
import json

ann_dir = './annotated_json_cleaned/'
stanford_coref_dir = './parse_coref_openie/'


subj_errors = 0 
obj_errors = 0
rel_errors = 0

for file in os.listdir(ann_dir):

	if not file.endswith(".json"):
		continue

	opfile = open(stanford_coref_dir + file, 'w')

	with open(os.path.join(ann_dir, file), 'r') as f:
		ann_json = json.load(f)

		print(file)


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
				mention['ner'] = []

				for idx in range(start_idx -1 , end_idx - 1):
					mention['pos'].append(ann_json['sentences'][sent_num -1]['tokens'][idx]['pos'])
					mention['ner'].append(ann_json['sentences'][sent_num -1]['tokens'][idx]['ner'])






		for sentence in ann_json['sentences']:
			for triple in sentence["openie"]:
				subj_span = triple['subjectSpan']
				obj_span = triple['objectSpan']
				rel_span = triple['relationSpan']

				del triple['subjectSpan']
				del triple['objectSpan']
				del triple['relationSpan']

				triple['pos'] = {}
				triple['ner'] = {}


				if len(triple['subject'].split()) != subj_span[1] - subj_span[0]:
					print(triple['subject'])
					print(subj_span)
					subj_errors +=1 

				if len(triple['object'].split()) != obj_span[1] - obj_span[0]:
					obj_errors +=1

				if len(triple['subject'].split()) != rel_span[1] - rel_span[0]:
					rel_errors +=1

				triple['pos']['subject'] = [sentence['tokens'][x]['pos'] for x in range(subj_span[0], subj_span[1])]
				triple['ner']['subject'] = [sentence['tokens'][x]['ner'] for x in range(subj_span[0], subj_span[1])]

				triple['pos']['relation'] = [sentence['tokens'][x]['pos'] for x in range(rel_span[0], rel_span[1])]
				triple['ner']['relation'] = [sentence['tokens'][x]['ner'] for x in range(rel_span[0], rel_span[1])]

				triple['pos']['object'] = [sentence['tokens'][x]['pos'] for x in range(obj_span[0], obj_span[1])]
				triple['ner']['object'] = [sentence['tokens'][x]['ner'] for x in range(obj_span[0], obj_span[1])]
			del sentence['parse']
			del sentence['tokens']


		opfile.write(json.dumps(ann_json))


print(subj_errors, obj_errors, rel_errors)


