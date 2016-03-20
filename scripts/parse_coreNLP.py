import sys
import glob 
import os
import random
import json



fdir =  '../LDA/annotated_dataset/*.json'
op_dir = '../LDA/annotated_json_cleaned/'



for jsonfile in glob.glob(fdir):
	op_json_file  = op_dir + jsonfile.split('/')[-1].split('.')[0] + '.json'
	print(op_json_file)
	
	corejson = None
	with open(jsonfile, 'r') as fh:
		corejson = json.loads(fh.read())

	
	for sentence in corejson['sentences']:
		del sentence['basic-dependencies']
		del sentence['collapsed-dependencies']
		del sentence['collapsed-ccprocessed-dependencies']
		del sentence['index']
		del sentence['sentiment']
		del sentence['sentimentValue']
		for token in sentence['tokens']:
			del token['index']
			del token['originalText']
			del token['characterOffsetBegin']
			del token['characterOffsetEnd'] 
			
			try:
				del token['speaker']
				del token['before']
				del token['after']

			except:
				pass

	
	

	with open(op_json_file, 'w') as oph:
		oph.write(json.dumps(corejson))



	
	

