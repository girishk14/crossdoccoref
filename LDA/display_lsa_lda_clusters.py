import json
import os
import sys
obj = None
with open('lsa_lda_results.json', 'r') as f:
	obj = json.loads(f.read())


json_dir = '../data/NYTimes/JSON/'

jsondescs = []
for txtfile in obj['docs']:
	#aprint(txtfile)
	parts = txtfile.split('/')
	fid = int(parts[-1].split('.')[0])
	jsonfile = parts[-2]	
	ctr = 0
	with open(json_dir + jsonfile + '.json', 'r') as jsonreader:
		for line in jsonreader:
			if ctr== fid:
				a = (json.loads(line))
				jsondescs.append(a)	
				break
			ctr+=1

	#print(jsondescs)


print(len(jsondescs))
for cluster in obj['lsa_clusters']:
	for article in obj['lsa_clusters'][cluster]:
		print(jsondescs[int(article)]['headline'])

	print('\n\n')

			
