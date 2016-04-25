import sys
import glob
import os
import random
import nltk
import json
import collections

json_dir = "./jsons/"

naive_clusters = {}

for jfile in os.listdir(json_dir):


	if jfile != "11_rel_coref_merged.json":
		continue

	jj = open(json_dir + jfile, 'r')
	cjson  = json.load(jj)
	cnt = 0

	for entity in cjson['corefs']:	


		cluster_id = entity['location'][0]

		if cluster_id not in naive_clusters.keys():	
			naive_clusters[cluster_id] = {'mentions':[], 'relations':[]}

		naive_clusters[cluster_id]['mentions'].append(entity['attributes'][0])

		for relation in entity['relations']:
			cnt+=1
			rel = {}
			if relation['role'] == 'subject':
				rel['target'] = relation['object']
			else:
				rel['target'] = relation['subject']
			
			rel['role'] = relation['role']
			rel['relation'] = relation['relation']
			rel['origin'] = len(naive_clusters[cluster_id]['mentions']) - 1
			naive_clusters[cluster_id]['relations'].append(rel)



	with open("naive_cluster_11.json", 'w') as oj:
		oj.write(json.dumps(naive_clusters))













