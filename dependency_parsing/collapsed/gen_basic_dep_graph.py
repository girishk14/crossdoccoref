import sys
import os
import json


json_dir = 'annotated_dataset/'


for ann_json in os.listdir(json_dir):

	if ann_json!='11.txt.json':
		continue

	node_ctr = 0
	print(ann_json)
	iff = open(json_dir + ann_json)

	ann = json.load(iff)

	graph = {'nodes':[], 'edges':[]}
	
	for idx,sentence in enumerate(ann['sentences']):
		sent_base_ctr = node_ctr

		root = {'label':'ROOT', 'id':node_ctr,'group':idx}
		graph['nodes'].append(root)
		node_ctr+=1
		for token in sentence['tokens']:
			node = {'label': token['word'], 'id':node_ctr, 'group':idx}
			node_ctr+=1
			graph['nodes'].append(node)


		for dependency in sentence['collapsed-ccprocessed-dependencies']:
			edge = {'label':dependency['dep'], 'from':dependency['governor'] + sent_base_ctr, 'to':sent_base_ctr + dependency['dependent']}
			graph['edges'].append(edge);

		break


with open('11_graph.json', 'w') as of:
	of.write(json.dumps(graph))





