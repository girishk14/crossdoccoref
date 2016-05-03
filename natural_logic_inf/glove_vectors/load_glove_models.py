import numpy
import json
from scipy import spatial


with open('vocab.json', 'r') as ifile:
	vocab = json.loads(ifile.read())


glove = numpy.load("vectorimage.npy")


while(True):

	print("\n\nOptions : \n1. Type a word to see its vector \n 2. Type two words space separated to find the cosine distance ")


	ip = raw_input()

	ip = ip.split();

	if len(ip) == 1:

		if ip[0] in vocab:
			idx = vocab[ip[0]]
			print(glove[idx])

		else:
			print("Out of vocab!")


	else:

		if ip[0] in vocab and ip[1] in vocab:
			vec1 = glove[vocab[ip[0]]]
			vec2 = glove[vocab[ip[1]]]
			sim = 1 - spatial.distance.cosine(vec1, vec2)
			print(sim)

		else:
			print("Out of vocab!")


	
