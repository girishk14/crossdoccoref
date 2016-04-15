import os
import sys
import json



def read_cluster_json():
	cluter_json = None
	with open('temp2.json','r') as f:
		cluster_json = json.loads(f.read())
	count = len(cluster_json.keys())
	print count
	with open('temp6.json','r') as f:
		cluster_json1 =json.loads(f.read())
	print cluster_json1.keys()
	for items in cluster_json1:
		cluster_json[str(count+1)]=cluster_json1[items]
		count+=1


	print cluster_json.keys()
	

	graph = {}
	graph['nodes']  =  []
	graph['edges'] = []


	node_dictionary = {}


	entity_counter =  0
	for cluster_member in cluster_json:
		for subj in cluster_json[cluster_member].keys():
			
			if subj in node_dictionary and node_dictionary[subj]['group']!='Common' and  node_dictionary[subj]['group'] != cluster_member:
				node_dictionary[subj]['group'] = 'Common'
			else:
				node_dictionary[subj] = {}
				node_dictionary[subj]['id'] = entity_counter
				entity_counter+=1
				node_dictionary[subj]['group'] = cluster_member

				for (rel, obj) in cluster_json[cluster_member][subj]:
					if obj in node_dictionary and node_dictionary[obj]['group']!='Common' and  node_dictionary[obj]['group'] != cluster_member:
						node_dictionary[obj]['group'] = 'Common'
					else:
						node_dictionary[obj] = {}
						node_dictionary[obj]['id'] = entity_counter
						entity_counter+=1	
						node_dictionary[obj]['group'] = cluster_member

					edge_obj = {}
					edge_obj['from'] = node_dictionary[subj]['id']
					edge_obj['to'] = node_dictionary[obj]['id']
					edge_obj['label'] = rel
					graph['edges'].append(edge_obj)


	for node in node_dictionary.keys():
		node_obj = {}
		node_obj['id'] = node_dictionary[node]['id']
		node_obj['group'] = node_dictionary[node]['group']
		node_obj['label'] = node
		graph['nodes'].append(node_obj)





		with open('visjson.json', 'w') as f:
			f.write(json.dumps(graph))




					

read_cluster_json()
