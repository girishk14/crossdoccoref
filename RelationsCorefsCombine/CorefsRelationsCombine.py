import sys
import glob
import os
import random
import nltk
import json
import collections

ann_dir = './annotated_json_cleaned/'
stanford_coref_dir = './parse_coref_openie/'


subj_errors = 0 
obj_errors = 0
rel_errors = 0



dictCorefRelations ={}
with open('11.json', 'r') as f:
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
	else:
		dictResultOpenIEFinal [int(tuples[0][0])].append(tuples[1])
with open('dictOpenIE.json', 'w') as f:
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

# print dictCorefResultSorted
# sys.exit()


with open('dictCorefs.json', 'w') as f:
	f.write(json.dumps(dictCorefResultSorted))


dictCorefOpenIE={}

for coreTuples in dictCorefResultSorted['corefs']:
	print coreTuples



# dictCorefOpenIE={}
# for corefTuples in dictCorefResultSorted['corefs']:
# 	list1=[]
# 	if corefTuples[0][0] not in dictCorefOpenIE:
# 		dictCorefOpenIE[corefTuples[0][0]] =[]
# 	else:
# 		if corefTuples[0][0] in dictResultOpenIEFinal.keys():
# 			print len(dictResultOpenIEFinal[corefTuples[0][0]])
# 			dictCorefOpenIE[corefTuples[0][0]].append(dictResultOpenIEFinal[corefTuples[0][0]])

# print dictCorefOpenIE
# sys.exit()

dictFinalRelations={}
countCoref=1
for corefs in dictCorefOpenIE:
	for lists in dictCorefOpenIE[corefs]:
		print len(lists)
		# print lists[0]['subject']+ " "+ lists[0]['relation']+" "+ lists[0]['object']


print dictFinalRelations


