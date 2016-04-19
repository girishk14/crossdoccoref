import sys
import os
import random
import json

coref_json = None
openie_json = None

json_dir = "jsons/11/"

with open(json_dir+"dictCorefs.json","r") as f:
	coref_json = json.load(f)


with open(json_dir +"dictOpenIE.json","r") as f:
	openie_json = json.load(f)



for entity in coref_json['corefs']:
	entity['relations'] = []
	sent_number = entity['location'][1]
	#print(sent_number)
	try:
		for relation in openie_json[str(sent_number)]:
			entity['relations'].append(relation)
	except:
		continue

with open(json_dir + "rel_coref_merged.json", "w") as opf:
	opf.write(json.dumps(coref_json))


