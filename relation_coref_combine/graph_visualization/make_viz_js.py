import os
import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')


json_dir = "../"
coref_dir = "../coreference_graphs/"



def find_target_in_graph(graph, target):
	for node in graph['nodes']:
		if node['label'] in target or target in node['label']:
			return node['id']

	return -1
  

for jsonfile in os.listdir(json_dir):
	
	if "naive" not in jsonfile:
		continue

	graph = {'nodes':[], 'edges':[]}
	node_ctr = 0

	if not jsonfile.endswith('11.json'):
		continue
		
	with open(json_dir + jsonfile, 'r') as f:

		print(jsonfile)
		print(graph)
		ann_json = json.load(f)

		for chain_id in ann_json:
			chain_base_id = node_ctr
			for i,chain_entity in enumerate(ann_json[chain_id]['mentions']):
				nodeobj = {'id':  node_ctr, 'label': chain_entity, 'group':chain_id}
				node_ctr+=1
				graph['nodes'].append(nodeobj)
				graph['edges'].append({"from":chain_base_id + i, "to": chain_base_id + ((i+1)%len(ann_json[chain_id]['mentions']))})	


			for rel in ann_json[chain_id]['relations']:
				edge = {}
				ix = find_target_in_graph(graph, rel['target'])
				if ix >= 0 :
					edge['to'] =  ix


				else:
					nodeobj = {'id': node_ctr, 'label':rel['target'], 'group':'indep_targets'}
					graph['nodes'].append(nodeobj)
					edge['to'] = node_ctr
					node_ctr+=1

				edge['from'] = chain_base_id + rel['origin']
				edge['label'] = rel['relation']
				graph['edges'].append(edge)


				

		with open(coref_dir + jsonfile, 'w') as wf:
			wf.write(json.dumps(graph))


