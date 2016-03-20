import sys
from nltk.corpus import wordnet as wn

def is_polysemous(word): 
	if(len(wn.synsets(word)) > 1):#more than 1 sense	
		return True
	else:
		return False



print(is_polysemous(sys.argv[1]))
