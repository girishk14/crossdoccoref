import sys
import numpy
import random



sys.path.append("../../skip-thoughts")
import skipthoughts
import json

def extract_sentence_vectors(model):

	sentences = []
	selected_jsons = []
	ifile = open('../../snli_1.0/snli_1.0_train.jsonl', 'r')
	
	

	for idx,line in enumerate(ifile):
	#	print(idx)
		dropout_chance = random.random()
		if dropout_chance <0.1:			
			jj = json.loads(line)
			sentences.append(jj['sentence1'])
			sentences.append(jj['sentence2'])
			selected_jsons.append(jj)


	print(len(sentences), len(selected_jsons))

	#sys.exit()

	vectors = skipthoughts.encode(model, sentences)
 	sent_pair_vectors =  numpy.reshape(vectors, (len(vectors)/2, len(vectors[0]) * 2))
	
	print(sent_pair_vectors.shape)
	numpy.save("sentence_pair_vectors.npy", sent_pair_vectors)
	with open('selected_sentence_pairs.json','w') as f:
		for jsons in selected_jsons:
			f.write(json.dumps(jsons))
			f.write('\n')	

def main():
	model = skipthoughts.load_model()
	extract_sentence_vectors(model)



if __name__ == '__main__':
	main()
