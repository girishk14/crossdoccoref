import sys
import os
import json


json_dir = 'annotated_dataset/'


graph = {'nodes':[], 'edges':[]}
	
for ann_json in os.listdir(json_dir):

	# if ann_json!=sys.argv[1]:
	# 	continue

	# if ann_json!='11.txt.json':
	# 	continue

	node_ctr = 0
	print(ann_json)
	iff = open(json_dir + ann_json)

	ann = json.load(iff)

	for idx,sentence in enumerate(ann['sentences']):
		sent_base_ctr = node_ctr
		# if idx!=int(sys.argv[2]):
		# 	continue

		# if idx > 2:
		# 	continue

		if  not "Abdeslam" in [token['word'] for token in sentence['tokens']]:
			continue

		root = {'label':'ROOT', 'id':node_ctr,'group':idx}
		graph['nodes'].append(root)
		node_ctr+=1
		for token in sentence['tokens']:
			node = {'label': token['word'], 'id':node_ctr, 'group':idx}
			node_ctr+=1
			graph['nodes'].append(node)


		for dependency in sentence['basic-dependencies']:
			edge = {'label':dependency['dep'], 'from':dependency['governor'] + sent_base_ctr, 'to':sent_base_ctr + dependency['dependent']}
			graph['edges'].append(edge);

		# break


with open('11_graph.json', 'w') as of:
	of.write(json.dumps(graph))





