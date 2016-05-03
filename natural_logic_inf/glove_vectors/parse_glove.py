import numpy
import json
import sys

vocab = {}

glove = numpy.zeros((2000000, 300))


with open("vectors.txt", 'r') as f:

	for idx, line in enumerate(f):
		parts = line.split();
		vocab[parts[0]] = idx;

		glove[idx] =  parts[1:];


		if idx%10000 == 0:
			print(idx)

#	print(vocab)
	
	#numpy.save("vectorimage.npy", glove)		

	with open("vocab.json", 'w') as ojson:
		ojson.write(json.dumps(vocab))
