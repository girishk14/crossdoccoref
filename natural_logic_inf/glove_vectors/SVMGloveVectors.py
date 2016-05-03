from sklearn import svm
import numpy
import sys
import json
X= numpy.load('glove_sent_vectors.npy')

print(X.shape)

YDict=[]


with open ('./snli_1.0/snli_1.0_train.jsonl','r')as f:
	YDict=f.readlines()


labels=[]
for lines in YDict:
	dict1=json.loads(lines)
	labels.append(dict1['gold_label'])



clf=svm.SVC(kernel='rbf',C=5.0, gamma=0.1, cache_size = 1000)

clf.fit(X[0:10000],labels[0:10000])

count=0
countCorrect=0
for i in range(20000, 25000):
	count+=1
	if clf.predict(X[i])[0]==labels[i]:
		countCorrect+=1
	#	print countCorrect
print (countCorrect*1.0)/count


