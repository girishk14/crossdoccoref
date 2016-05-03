import numpy
import sys
import os

import json
import itertools


def main():
	file_dir = 'annotated/'
	
	sentences = []
	
	for jfile in os.listdir(file_dir):
		if jfile!='11.txt.json' and jfile!='12.txt.json':
			continue
		ff = open(file_dir + jfile, 'r')
		jj = json.load(ff)
		print(jfile)
		for idx, sent in enumerate(jj['sentences']):
			words = [token['word'] for token in sent['tokens']]
			sent_string = ' '.join(word for word in words)
			
			sent_obj = {}
			sent_obj['sent'] = sent_string
			sent_obj['file_name'] = jfile
			sent_obj['sent_no']  = idx
					
			sentences.append(sent_obj)


	combs = itertools.combinations(sentences, 2)
			
	comblist = []
	for comb in combs:
		comblist1=[]
		comblist.append([comb[0],comb[1]])
		#comblist.append(comblist1)
	
	print len(comblist)
	
	with open('op.json', 'w') as op:
		for combos in comblist:
			op.write(json.dumps(combos))
			op.write('\n')

if __name__ == '__main__':
	main()

