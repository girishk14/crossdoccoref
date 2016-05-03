import json
import copy


with open('SentPairlabelOutput.json','r') as f:
	list1=json.loads(f.read())

dict2={}
list2=[]

with open('ManualAnnotation.json', 'w') as f:
for line in list1:
	if 'manualLabel1' not in line.keys() and manualLabel2 not in line.keys():
		print line['sentence1']
		print line['sentence2']
		print line['label']
		manualLabel=input('enter Label-- E, N, C ')
		if manualLabel=='E':
			line['manualLabel']='entailment'
		if manualLabel=='N':
			line['manualLabel']='neutral'
		if manualLabel=='C':
			line['manualLabel']='contradiction'
		else:
			print 'Enter valid Input'
		list2.append(
	
