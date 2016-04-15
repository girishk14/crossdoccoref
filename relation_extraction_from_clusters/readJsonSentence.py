import json
import os
from nltk import sent_tokenize, word_tokenize, pos_tag, ne_chunk
import nltk

import sys
reload (sys)
sys.setdefaultencoding("utf-8")
count =0


path = "./clusters/"
op_path = "./relations/"




for cluster in os.listdir(path):
	ClusterRelations = {}
	listJsons = []
	dir_name = path + cluster + '/'
	#print("Cluster", cluster)
	count = 0
	for filename in sorted(os.listdir(dir_name)):
		if filename.startswith('.'):
			continue
		with open(os.path.join(dir_name, filename)) as f:
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
		ClusterRelations[str(count)]=NodeRelations
	#	print(ClusterRelations.keys())
	strjson=json.dumps(ClusterRelations)
	with open(os.path.join(op_path, cluster + '.json'),'w') as of:
		print(of)
		of.write(strjson)
#		sys.exit()


