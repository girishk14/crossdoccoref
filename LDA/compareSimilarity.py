from gensim import corpora, models, similarities
import os
import sys
import gensim
import logging
import numpy
import string
import glob
import string
import json
import random
from nltk.corpus import stopwords
from collections import defaultdict
from nltk.stem.porter import *
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
reload (sys)
sys.setdefaultencoding("utf-8")

op_file =open( 'lsa_lda_results.json', 'w')

op_json = {}

op_json['docs'] = []

documents=[]
dict1={}

#path = "../data/NYTimes/Text/20151116_to_20151116/*.txt"
path = 'dataset/*.txt'

file_order =  []


filelist = glob.glob(path)
print(filelist)	
random.shuffle(filelist)
print(filelist)

for filename in filelist:
	print(filename)
	with open(filename) as f:
		op_json['docs'].append(os.path.realpath(filename))
		documents.append(f.read().decode('unicode_escape').encode('ascii','ignore').replace("\n","").translate(None, string.punctuation))

stoplist=["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", 
"because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", 
"besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", 
"cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", 
"down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", 
"etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", 
"fill", "find", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", 
"front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", 
"hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", 
"hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", 
"latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", 
"mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", 
"neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", 
"now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", 
"otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", 
"same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", 
"since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", 
"somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", 
"then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", 
"thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", 
"to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", 
"up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", 
"whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", 
"which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", 
"without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the", "advertisement","said","mr", "mrs" ]

stop = stopwords.words('english')
stoplist.extend(stop)


# stoplist = set('for a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]  for document in documents]

stemmer = PorterStemmer()
texts = [[stemmer.stem(word) for word in text] for text in texts]


frequency = defaultdict(int)
for text in texts:
	for token in text:
		frequency[token] += 1



texts = [[token for token in text if frequency[token] > 1] for text in texts]

#print(texts)



#print(texts)
#sys.exit()

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('deerwester.mm', corpus)
mm = gensim.corpora.MmCorpus('deerwester.mm')
tfidf = models.TfidfModel(mm)
corpus_tfidf = tfidf[mm]


'''
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=6) # initialize an LSI transformation
# sys.exit()

corpus_lsi = lsi[corpus_tfidf]

#lsi.print_topics(6)


dict2={}
count=0


for doc in corpus_lsi:
	print doc
	maxC=-20
	l=-1
	for tup in doc:
		if tup[1] > maxC:
			maxC=tup[1]
			l=tup[0]
	dict2[count]=l
	count+=1
	# print "count is ", count, "   ", tup[0]
# print dict2
dictF={}
for entity in dict2.keys():
	event=dict2[entity]
	if event in dictF.keys():
		dictF[event].append(entity)
	else:
		dictF[event]=[]
		dictF[event].append(entity)
#print dictF


op_json['lsa_cluster'] = dictF

 #219 doc, 20 topics=20
	# print (doc)
'''
lda = gensim.models.ldamodel.LdaModel(corpus=mm, id2word=dictionary, num_topics=8, update_every=1, chunksize=2, passes=60)

corpus_lda = lda[corpus]#_tfidf]


lda.print_topics(8)


print(corpus_lda)


#sys.exit()
dict3={}
count3=0






for doc in corpus_lda:
	print doc
	maxC=-20
	l=-1
	for tup in doc:
		if tup[1] > maxC:
			maxC=tup[1]
			l=tup[0]
	dict3[count3]=l
	count3+=1
	# print "count is ", count, "   ", tup[0]
# print dict2
dictF3={}




for entity in dict3.keys():
	event=dict3[entity]
	if event in dictF3.keys():
		dictF3[event].append(entity)
	else:
		dictF3[event]=[]
		dictF3[event].append(entity)



for cluster in dictF3:
	for article in dictF3[cluster]:
		print(op_json['docs'][int(article)])
	print("\n")




op_json['lda_clusters'] = dictF3

op_file.write(json.dumps(op_json,indent=1))

