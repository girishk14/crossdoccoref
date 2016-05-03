import numpy as np
import random
import copy
import math
from _sqlite3 import Row


class AnnBackProp(object):
    layerCount=0
    shape=None
    weights=[]


    def __init__(self, layerTuple):
        self.layerCount= len(layerTuple)-1
        self.shape= layerTuple
        
        self._layerInput=[]
        self._layerOutput=[]
        self._previousWeightDelta=[]
        for (l1,l2) in zip(layerTuple[:-1],layerTuple[1:]):
            self.weights.append(np.random.normal(scale=0.2,size=(l2,l1+1)))
            self._previousWeightDelta.append(np.zeros([l2,l1+1]))
    
    def readFile(self, str1):
        lines=[]
        for line in file(str1, 'r'):
            line1=[]
            for str2 in line.rstrip('\n').split(","):
                line1.append(str2)
            lines.append(line1)
        
#         for i in range(0,1000):       
#             random.shuffle(lines)
#         print lines
        return lines
    def readFileShuffle(self, str1):
        lines=[]
        for line in file(str1, 'r'):
            line1=[]
            for str2 in line.rstrip('\n').split(","):
                line1.append(str2)
            lines.append(line1)
        
        for i in range(0,500):       
            random.shuffle(lines)
#         print lines
        return lines
    
    
    def FeedForward(self,input):
    
        lnCases = input.shape[0]
       
        
        self._layerInput=[]
        self._layerOutput=[]
        
        for index in range(self.layerCount):
            if index==0:

                layerInput = self.weights[0].dot(np.vstack([input.T,np.ones([1,lnCases])]))
            else:

                layerInput=self.weights[index].dot(np.vstack([self._layerOutput[-1],np.ones([1,lnCases])]))
            self._layerInput.append(layerInput)
            self._layerOutput.append(self.sgm(layerInput))

        return self._layerOutput[-1].T
    
    def BackPropLearn(self,input,target, learnRate=0.2,momentum=0.4):
        delta=[]
        lnCases=input.shape[0]
        cas=[]

        self.FeedForward(input)
        
        for index in reversed(range(self.layerCount)):
            if index == self.layerCount-1:
                output_delta=self._layerOutput[index]-target.T
                error=np.sum(output_delta**2)
                delta.append(output_delta*self.sgm(self._layerInput[index],True))
            else:
                deltaBack=self.weights[index+1].T.dot(delta[-1])
                delta.append(deltaBack[:-1,:]*self.sgm(self._layerInput[index],True))
                
        for index in range(self.layerCount):
            delta_index=self.layerCount-1-index
            if index==0:
                layerOutput=np.vstack([input.T,np.ones([1,lnCases])])
            else:
                layerOutput =np.vstack([self._layerOutput[index-1],np.ones([1,self._layerOutput[index-1].shape[1]])])
                
            curweightDelta=np.sum(\
                               layerOutput[None,:,:].transpose(2,0,1)*delta[delta_index][None,:,:].transpose(2,1,0)\
                               ,axis=0)
            weightDelta =learnRate*curweightDelta +momentum*self._previousWeightDelta[index]
            self.weights[index]-=weightDelta
            self._previousWeightDelta[index] =weightDelta
        return error
    
    def getError(self,input,target):
        lnCases=input.shape[0]
        
        self.FeedForward(input)
        output_delta=self._layerOutput[self.layerCount-1]-target.T
        error=np.sum(output_delta**2)
        return error
        
    
    
    def sgm(self,x,Derivative=False):
        if not Derivative:
            return 1/(1+np.exp(-x))
        else:
            out=self.sgm(x)
            return out*(1-out)
    def getMeanStd(self,listOfAttributes,listOfRows):
        dictMeanSigma={}
        for attribute in listOfAttributes:
            listColumn=[]
            if (attribute[1]=='C'):
                for row in listOfRows:
                    if row[int(attribute[2])] !='?':
#                         print row[int(attribute[2])]
                        listColumn.append(float((row[int(attribute[2])])))
                data = np.array(listColumn)
                mean = sum(listColumn)/float(len(listColumn))
#             print mean
                stdev=np.std(data)
                listStats=[]
                listStats.append(mean)
                listStats.append(stdev)
                dictMeanSigma[int(attribute[2])]=listStats
        return dictMeanSigma
    def getMaxDiscrete(self,listOfAttributes,listOfRows):
        dictMaxDiscrete={}
        for attribute in listOfAttributes:
            listColumn=[]
            if (attribute[1]=='D'):
                for row in listOfRows:
                    if row[int(attribute[2])] !='?':
                        listColumn.append((row[int(attribute[2])]))
                str2=max(x for x in listColumn if listColumn.count(x) > 1)
                dictMaxDiscrete[int(attribute[2])]=str2
        return dictMaxDiscrete
        
        
    
    def makeInputLayer(self,listOfRows, listOfAttributes):
        numNodes=-1
        dictNodes={}
        for attribute in listOfAttributes:
            if attribute[0]!='Diagnosis' and attribute[0]!='ID Number':
                if attribute[1]=='C':
                    
                    dictNodes[attribute[0]]=numNodes+1
                    numNodes+=1
                else:
                    for value in attribute[4:]:
                        
                        numNodes+=1
                        dictNodes[value+"-"+attribute[2]]=numNodes
        return dictNodes
    
    def makeFractionData(self,listOfRows, fraction):
        listFirst=[]
        listSecond=[]
        listFinal=[]
        for i in range(0,int(fraction*len(listOfRows))):
            listFirst.append(listOfRows[i])
        for i in range(0,500):       
            random.shuffle(listFirst)
        listFinal.append(listFirst)
        for i in range(int(fraction*len(listOfRows))+1,len(listOfRows)):
            listSecond.append(listOfRows[i])
        for i in range(0,500):       
            random.shuffle(listSecond)   
        listFinal.append(listSecond)   
        return listFinal
    def dictOutput(self,str2):
        list1=self.readFile(str2)
        dict1={}
        for row in list1:
            dict1[int(row[0])]=row[1]
        return dict1
            
    
    def formInputOutPut(self,listOfAttributes,listOfRows,dictOut,dictIn):
        dictStats=self.getMeanStd(listOfAttributes, listOfRows)
        dictInputLayer=dictIn
        listInputs=[]
        listOutputs=[]

        listF=[]

        for row in listOfRows:
            dict1={}
            dict2={}
            str1=""
            for val in range(0,len(row)):
                if listOfAttributes[val][1]=='C':

                    dict1[dictInputLayer[listOfAttributes[val][0]]] = float(float(row[val])-dictStats[int(listOfAttributes[val][2])][0])/float(dictStats[int(listOfAttributes[val][2])][1])
                elif listOfAttributes[val][1]=='D':
                    dict1[dictInputLayer[row[val]+"-"+listOfAttributes[val][2]]] = float(1)
                else:
                    str1=row[val]
                    
            list1=[]
            list2=[]

#             print len(dictIn)
            for numNode in range (0,len(dictIn)):
                if numNode in dict1.keys():
                    list1.append(dict1[numNode])
                else:
                    list1.append(0.0)

            listInputs.append(list1)
            for numNode in range(0,len(dictOut)):

                if dictOut[numNode]!=str1:
                    list2.append(0.0)
                else:
                    list2.append(1.0)

            listOutputs.append(list2)
        listF.append(listInputs)

        listF.append(listOutputs)
        return listF
    def findAccuracy(self,input,output):

        numCorrect=0
        numTotal=0
        for i in range(0,len(self.FeedForward(input))):
            numTotal+=1
            list1=self.FeedForward(input)[i].tolist()
            list2=output[i].tolist()
            if (list1.index(max(list1)) == list2.index(max(list2))):
                numCorrect+=1
        return float(numCorrect)/float(numTotal)

    def divideTenBuckets(self, listOfRows):
        
        list10buckets= lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
        l1= list10buckets(listOfRows,len(listOfRows)/10+1)
        return l1
    def getEachFold(self,list10buckets,i):
        list90=[]
        list10=[]
        list1=[]
        for j in range(0, len(list10buckets)):
            if (j!=i):
                for k in range (0, len(list10buckets[j])):
                    list90.append(list10buckets[j][k])
                else:
                    list10.append(list10buckets[j][k])
        list1.append(list90)
        list1.append(list10)
        return list1
            
    def handleMissingValues(self,listOfAttributes,listOfRows):
        dictMaxDiscrete= self.getMaxDiscrete(listOfAttributes, listOfRows)
        dictMeanSigma =self.getMeanStd(listOfAttributes, listOfRows)
        for row in listOfRows:
            for i in range(0, len(row)):
                if row[i]=='?':
                    if listOfAttributes[i][1]=='D':
                        row[i]=dictMaxDiscrete[i]
                    if listOfAttributes[i][1]=='C':
                        row[i]=str(dictMeanSigma[i][0])
        return listOfRows
                        
                        
                      
    

        

if __name__ == '__main__':
    print"enter layer size"
    t1=tuple(map(int,raw_input().split(',')))
    bpn =AnnBackProp(t1)
    
    
    list1 =[]
    categoryFile = input('Input categories/diagnosisData.txt ')
    dictOut=bpn.dictOutput(categoryFile)
    dataFile = input('Input datData.txt ')
    
    listOfRowsI=bpn.readFileShuffle(dataFile)
    for i in range(0,78):       
        random.shuffle(listOfRowsI)
    
    NameFile = input('Input NameData.txt ')
    
    listOfAttributes=bpn.readFile(NameFile)
    listOfRows=bpn.handleMissingValues(listOfAttributes, listOfRowsI)
    
    learnRate=input('learning rate : ')
    momentum = input('momentum : ')
    
    
    dictIn=bpn.makeInputLayer(listOfRows, listOfAttributes)
    print len(dictIn.keys())
    buckets10=bpn.divideTenBuckets(listOfRows)
    errList=[]
    print "10 fold cross validation:"
    for fold in range(0,10):
        bpn1 =AnnBackProp(t1)
        list2=bpn1.getEachFold(buckets10,fold)
        listTest=list2[1]
        #list2[0] is original 90, list2[1] is original 10
        listTrainValid=bpn1.makeFractionData(list2[0], 0.7)
        listTrain=listTrainValid[0]
        listValid=listTrainValid[1]
        
        
        ivInputOutPutTrain=bpn1.formInputOutPut(listOfAttributes, listTrain,dictOut,dictIn)
        ivInputTrain=np.array(ivInputOutPutTrain[0])
        ivTargetTrain=np.array(ivInputOutPutTrain[1])
        
        ivInputOutPutValid=bpn1.formInputOutPut(listOfAttributes, listValid,dictOut,dictIn)
        ivInputValid=np.array(ivInputOutPutValid[0])
        ivTargetValid=np.array(ivInputOutPutValid[1])
        
        ivInputOutPutTest=bpn1.formInputOutPut(listOfAttributes, listTest,dictOut,dictIn)
        ivInputTest=np.array(ivInputOutPutTest[0])
        ivTargetTest=np.array(ivInputOutPutTest[1])
        
        lnMax =100000
        lnErr=0.1
        errMax=10000000000
 
        err=bpn1.BackPropLearn(ivInputTrain, ivTargetTrain,learnRate,momentum)
       
        errValid=bpn1.getError(ivInputValid, ivTargetValid)/float(len(ivInputValid))
        i=0

#     lnErr=1e-5
        errPrev=copy.deepcopy(errValid)
        for i in range(lnMax-1):
            i+=1
            cas=[]
            random_item = random.randint(0, len(ivInputOutPutTrain[0])-1)
            InputRandom=[]
            OutPutRandom=[]
            InputRandom.append(ivInputOutPutTrain[0][random_item])
            OutPutRandom.append(ivInputOutPutTrain[1][random_item])
            inP=np.array(InputRandom)
            outP=np.array(OutPutRandom)

            
            err=bpn1.BackPropLearn(inP, outP,learnRate,momentum)
            err1=bpn1.getError(ivInputValid, ivTargetValid)/float(len(ivInputValid))

            if i >10000:

                break
            errPrev=copy.deepcopy(err1)

        print "Accuracy in Fold ",fold," on Validation","  :   ",bpn1.findAccuracy(ivInputValid,ivTargetValid)
        errFold=bpn1.findAccuracy(ivInputTest,ivTargetTest)
        print "On Test ","  :  ",errFold
        errList.append(errFold)
    data = np.array(errList)
    mean = sum(errList)/float(len(errList))
#             print mean
    stdev=np.std(data)
    stdErr=stdev/float(math.sqrt(10))
    CI=mean + 2.23* stdErr*100
    CI=mean - 2.23* stdErr*100
    print " iteration is ",i
    print " mean is ", mean
#     print stdev
    print "standarad error is ",stdErr
    print "confidence interval is " ,CI
        

          
