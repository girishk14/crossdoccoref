from sklearn import svm
import numpy
import sys
import json
import pickle
from sklearn.externals import joblib
X= numpy.load('sentence_pair_vectors.npy')
YDict=[]
with open ('selected_sentence_pairs.json','r') as f:
	YDict=f.readlines()
labels=[]
for dict1 in YDict:
	labels.append(json.loads(dict1)['gold_label'])
	
clf =svm.SVC(kernel='rbf',C=5.0,gamma=0.1)
clf.fit(X[0:6000],labels[0:6000])
countCorrect=0
count1=0
for i in range(6001,7000):
	count1+=1
	if (clf.predict(X[i])[0]==labels[i]):
		countCorrect+=1
		print countCorrect
print (countCorrect*1.0)/count1
joblib.dump(clf,'SVMFunction.pkl')
#print clf.predict([[2.,2.]])
