import json
import os
from nltk import sent_tokenize, word_tokenize, pos_tag, ne_chunk
import nltk

import sys
reload (sys)
sys.setdefaultencoding("utf-8")
NodeRelations1={}
count =0
path='./'+sys.argv[1]
print path
# path = './two'
listJsons=[]

for filename in sorted(os.listdir(path)):
	with open(os.path.join(path, filename)) as f:
		json_data=f.read()
		listJsons.append(json.loads(json_data))
for data in listJsons:
    NodeRelations={}
    for sentences in data['sentences']:
		if sentences['openie'] is not None:
			for openies in sentences['openie']:
				try:
					if openies['subject'] in NodeRelations:
						
						list1=[]
						list1.append(openies['relation'])
						list1.append(openies['object'])
						NodeRelations[openies['subject']].append(list1)
					else:
						NodeRelations[openies['subject']]=[]
						list1=[]
						list1.append(openies['relation'])
						list1.append(openies['object'])
						
						NodeRelations[openies['subject']].append(list1)
						
				except:
					pass
    count+=1
    NodeRelations1[str(count)]=NodeRelations
print NodeRelations1.keys()
strjson=json.dumps(NodeRelations1)
with open('temp6.json','w') as of:
	of.write(strjson)



