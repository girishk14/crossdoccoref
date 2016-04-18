import os
import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')


json_dir = "../annotated_json_cleaned/"
coref_dir = "../coreference_graphs/"


for jsonfile in os.listdir(json_dir):
	graph = {'nodes':[], 'edges':[]}
	node_ctr = 0

	if not jsonfile.endswith('11.json'):
		continue
		
	with open(json_dir + jsonfile, 'r') as f:

		print(jsonfile)
		print(graph)
		ann_json = json.load(f)

		for chain_id in sorted(ann_json['corefs']):

			chain_base_id = node_ctr
			for chain_entity in ann_json['corefs'][chain_id]:
				rep = chain_entity['isRepresentativeMention']
				nodeobj = {'id':  node_ctr, 'label':chain_entity['text'], 'group':chain_id, 'shadow':rep}
				node_ctr+=1
				graph['nodes'].append(nodeobj)

			# print("Chain id :", chain_id)
			if len(ann_json['corefs'][chain_id]) > 1 :
				for i in range(0, len(ann_json['corefs'][chain_id])):
				# print(i)
			#graph['edges'].append(zip(ann_json['corefs'][chain_id],ann_json['corefs'][chain_id][1:]))
			#raph['edges'].append((ann_json['corefs'][chain_id][len(ann_json['corefs'][chain_id])-1], ann_json['corefs'][chain_id][0]))
					graph['edges'].append({"from":chain_base_id + i, "to": chain_base_id + ((i+1)%len(ann_json['corefs'][chain_id]))})	




		print(graph)

		with open(coref_dir + jsonfile, 'w') as wf:
			wf.write(json.dumps(graph))


