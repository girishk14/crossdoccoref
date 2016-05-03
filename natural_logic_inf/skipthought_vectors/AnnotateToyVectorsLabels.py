import json
dict2 ={}

with open('outputToyVectors.json', 'r') as f:
	dict2=json.loads(f.read())
print dict2	
list1=[]

with open('./toy_vectors/op.json', 'r') as f:
	list1= f.readlines()
count =0
listFinal=[]
for line in list1:
	dict4= json.loads(line)
	dict3={}
        dict3['sentence1']=dict4[0]['sent']
	dict3['sentence2']=dict4[1]['sent']
	dict3['label']=dict2[str(count)]
	count+=1
	listFinal.append(dict3)
dictFinalOutput=json.dumps(listFinal)
with open('SentPairLabelOutput.json', 'w') as f:
	f.write(dictFinalOutput)




