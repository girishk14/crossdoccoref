from sklearn import svm
import numpy
import json
from sklearn.externals import joblib
clf=joblib.load('SVMFunction.pkl')
TestToyData= numpy.load('./toy_vectors/toy_pair_vectors.npy')
dict1={}
count1=0
for examples in TestToyData:
	dict1[count1]=clf.predict(examples)[0]
	print dict1[count1]
	count1+=1
with open('outputToyVectors.json','w') as f:
	f.write(json.dumps(dict1))

