import sys
import glob
import os
import random
import nltk
import json
import collections

ann_dir = './annotated_json_cleaned/'
stanford_coref_dir = './parse_coref_openie/'

jdir = "jsons/"

dictCorefRelations ={}
with open(jdir + sys.argv[1] + ".json", 'r') as f:
	dictCorefRelations=json.loads(f.read())

dictCorefs= dictCorefRelations['corefs']
listSentences=dictCorefRelations['sentences']
dictOpenIE={}
count=0
countSentence=0
for sentence in listSentences:
	for openIEs in sentence['openie']:
		dictOpenIE[(countSentence,count)] = openIEs
		count+=1
	countSentence+=1
dictResultOpenIE={}
# dictResultOpenIE['openie']=collections.OrderedDict(sorted(dictOpenIE.items()))
# print dictResultOpenIE
dictResultOpenIE['openie']= sorted(dictOpenIE.items())

dictResultOpenIEFinal={}   
for tuples in dictResultOpenIE['openie']:
	if int(tuples[0][0]) not in dictResultOpenIEFinal.keys():
		dictResultOpenIEFinal [int(tuples[0][0])]=[]
		dictResultOpenIEFinal [int(tuples[0][0])].append(tuples[1])

	else:
		dictResultOpenIEFinal [int(tuples[0][0])].append(tuples[1])
with open(jdir + sys.argv[1] + "_" + 'dictOpenIE.json', 'w') as f:
	f.write(json.dumps(dictResultOpenIEFinal))




dictCorefResult={}
corefCount=0
for corefs in dictCorefs:
	
	for coreDict in dictCorefs[corefs]:

		if (int(corefs),coreDict['sentNum']-1,coreDict['startIndex']-1, coreDict['endIndex']-1 ) not in  dictCorefResult.keys():
			dictCorefResult[(int(corefs),coreDict['sentNum']-1,coreDict['startIndex']-1, coreDict['endIndex']-1 ) ]=[coreDict['text'], coreDict['gender'], coreDict['number'], coreDict['type']]
		else:
			print "overWriting"

dictCorefResultSorted={}

dictCorefResultSorted['corefs']= sorted(dictCorefResult.items())
final_dict  =  {}
final_dict['corefs'] = []


for (location, attr) in dictCorefResultSorted['corefs']:
	entity = {}
	entity['location'] = location
	entity['attributes'] = attr
	final_dict['corefs'].append(entity)


with open(jdir + sys.argv[1] + "_" + 'dictCorefs.json', 'w') as f:
	f.write(json.dumps(final_dict))


coref_json = final_dict
openie_json = dictResultOpenIEFinal

for entity in coref_json['corefs']:
	entity['relations'] = []
	sent_number = entity['location'][1]
	#print(sent_number)
	try:
		for relation in openie_json[(sent_number)]:
			entity['relations'].append(relation)
	except:
		continue

with open(jdir + sys.argv[1] + "_" + "rel_coref_merged.json", "w") as opf:
	opf.write(json.dumps(coref_json))





























































