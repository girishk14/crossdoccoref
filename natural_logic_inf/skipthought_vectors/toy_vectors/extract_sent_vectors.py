import sys
import numpy
import random



sys.path.append("../skip-thoughts/")
import skipthoughts
import json

def extract_sentence_vectors(model):

	sentences = []
	selected_jsons = []
	ifile = open('op.json', 'r')
	
	

	for idx,line in enumerate(ifile):

		jj = json.loads(line)
		
		s1 = jj[0]
		s2 = jj[1]
		
		sentences.append(s1['sent'])
		sentences.append(s2['sent'])


	
	vectors = skipthoughts.encode(model, sentences)
 	sent_pair_vectors =  numpy.reshape(vectors, (len(vectors)/2, len(vectors[0]) * 2))
	
	print(sent_pair_vectors.shape)
	numpy.save("toy_pair_vectors.npy", sent_pair_vectors)

def main():
	model = skipthoughts.load_model()
	extract_sentence_vectors(model)



if __name__ == '__main__':
	main()
