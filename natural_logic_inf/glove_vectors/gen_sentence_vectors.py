import numpy
import json
import sys
import re
import spell_norvig
vocab = None
with open('vocab.json', 'r') as ifile:
	vocab = json.loads(ifile.read())
glove = numpy.load("vectorimage.npy")
sentences = []

word_count = 0
wrong = 0

def get_sentence_encoding(sent):
	global word_count
	global wrong
	vector_sum = numpy.zeros(300)	
	regex = re.compile('[^a-zA-Z]')
	sent  = regex.sub(' ', sent).strip()
	words = sent.split()
	word_count += len(words)
	for word in words:
		try:
			vector_sum += glove[vocab[word.strip().lower()]]
		except:
			wrong+=1
			pass


	return vector_sum


def main():
	fin = open('snli_1.0/snli_1.0_train.jsonl', 'r')

	for idx,line in enumerate(fin):
		jj = json.loads(line)
		sentences.append(jj['sentence1'])
		sentences.append(jj['sentence2'])
		
	arr =  numpy.zeros((len(sentences), 300))


	for idx, sent in enumerate(sentences):
			if idx % 5000 == 0:
				print("At" , idx)
			vec_sum = get_sentence_encoding(sent)
			arr[idx] = vec_sum
		

	x = numpy.reshape(arr, (len(sentences)/2, 600))

	numpy.save("glove_sent_vectors.npy", x)
	global wrong
	global word_count
	print("Error rate",  wrong/float(word_count))


if __name__ == '__main__':
	main()
	
