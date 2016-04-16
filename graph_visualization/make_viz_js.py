import os
import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')



def read_cluster_json():
	cluter_json = None
	with open('trial.json','r') as f:
		cluster_json =json.loads(f.read())
	
	graph = {}
	graph['nodes']  =  []
	graph['edges'] = []
	node_dictionary = {}

	entity_counter =  0

	for cluster_member in cluster_json:
		for subj in cluster_json[cluster_member].keys():


			if subj in node_dictionary and node_dictionary[subj]['group']!='Common' and  node_dictionary[subj]['group'] != cluster_member:
				node_dictionary[subj]['group'] = 'Common'
				node_dictionary[subj]['members'].append(cluster_member)
			elif subj not in node_dictionary:
				node_dictionary[subj] = {}
				node_dictionary[subj]['id'] = entity_counter
				entity_counter+=1
				node_dictionary[subj]['group'] = cluster_member
				node_dictionary[subj]['members'] = []
				node_dictionary[subj]['members'].append(cluster_member)



				for (rel, obj) in cluster_json[cluster_member][subj]:
					if obj in node_dictionary and node_dictionary[obj]['group']!='Common' and  node_dictionary[obj]['group'] != cluster_member:
						node_dictionary[obj]['group'] = 'Common'
						node_dictionary[obj]['members'].append(cluster_member)
					elif obj not in node_dictionary:
						node_dictionary[obj] = {}
						node_dictionary[obj]['id'] = entity_counter

						entity_counter+=1	
						node_dictionary[obj]['group'] = cluster_member
						node_dictionary[obj]['members'] = []
						node_dictionary[obj]['members'].append(cluster_member)

						if entity_counter == 19:
							print(node_dictionary.keys())




					edge_obj = {}
					edge_obj['from'] = node_dictionary[subj]['id']
					edge_obj['to'] = node_dictionary[obj]['id']
					edge_obj['label'] = rel
					print(edge_obj)
					graph['edges'].append(edge_obj)


	for node in node_dictionary.keys():
		node_obj = {}
		node_obj['id'] = node_dictionary[node]['id']
		node_obj['group'] = node_dictionary[node]['group']
		
		node_obj['label'] = node
		node_obj['members'] = node_dictionary[node]['members']
		print(node_obj)
		graph['nodes'].append(node_obj)

		with open('visjson.json', 'w') as f:
			f.write(json.dumps(graph))




					

read_cluster_json()
