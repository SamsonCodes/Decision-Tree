# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 10:24:24 2019

@author: Samson
"""
import random
import pandas as pd

dataset_url = 'http://mlr.cs.umass.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv'
data = pd.read_csv(dataset_url, sep=';')
raw_data = data.values

def getRanges(dataSet):
    range_min = []
    range_max = []
    #print(len(dataSet))
    for f in range(0, len(dataSet[0])): #for every feature
        range_min.append(dataSet[0][f]) #add the first value of the feature to the range_min list
        range_max.append(dataSet[0][f]) #add the first value of the feature to the range_max list
        for x in range(0, len(dataSet)): #for every data point
            if(dataSet[x][f] < range_min[f]): #if current value of feature smaller then the min
                range_min[f] = dataSet[x][f] #update the min
            if(dataSet[x][f] > range_max[f]): #if current value of feature bigger then the max
                range_max[f] = dataSet[x][f] #update the max
    return [range_min, range_max]

def printDataStats(dataSet):    
    #print(data.columns)
    print("len(dataSet) =",len(dataSet))
    #print("len(dataSet)[0] =",len(dataSet[0]))
    """
    ranges = getRanges(dataSet)
    range_min = ranges[0]
    range_max = ranges[1]
    for x in range(0,len(range_min)):
        print("feature",x, ", min=","{:.2f}".format(range_min[x]), ", max=","{:.2f}".format(range_max[x]))
    #print(dataSet)
   
    for x in range(0,10):
        for y in range(0, len(dataSet[0])):
            print("{:.2f}".format(dataSet[x][y]), ", ", end="")
        print("\n")
        
    """
    #print("\n")

class Tree:
    def __init__(self):
        self.name = "Tree"
        self.nodes = []      
        self.depth = 1
        maxDepth = 4
        index = 0          
        parentNode = Node(index, self.depth, raw_data)  
        index+=1        
        self.nodes.append(parentNode)
        while(self.depth < maxDepth):
            #print("self.depth=",self.depth, "len(self.nodes)=",len(self.nodes))
            for x in range(0, len(self.nodes)):
                #print("x=",x,",len(self.nodes[x].dataSet)=",len(self.nodes[x].dataSet))
                if(self.nodes[x].layer == self.depth and len(self.nodes[x].dataSet) >= 2):    
                    self.nodes[x].split()
                    subsets = getSubsets(self.nodes[x].dataSet, self.nodes[x].feature, self.nodes[x].value)
                    if not (hasEmptySets(subsets)):
                        child1 = Node(index, self.depth+1, subsets[0])
                        index+=1
                        self.nodes.append(child1)
                        child2 = Node(index, self.depth+1, subsets[1])
                        index+=1
                        self.nodes.append(child2)
            self.depth+=1        
    def printTree(self):        
        for layer in range(1, self.depth + 1):
            for node in self.nodes:
                if(node.layer == layer):
                    if(node.feature != -1):
                        print("||",node.name,":",data.columns[node.feature],"<","{:.2f}".format(node.value),"gini =","{:.2f}".format(node.gini),"size =",len(node.dataSet),"||",end = "")
                    else:
                        print("||",node.name,":","size =",len(node.dataSet),"||",end = "")
            print("\n")     
    def printSubsets(self):        
        for node in self.nodes:
            if(node.layer == self.depth):
                print(node.name)
                printDataStats(node.dataSet)
                print()
        print("\n") 

class Node:
    def __init__(self, index, layer, dataSet):
        self.name = "Node" + str(index)
        self.layer = layer      
        self.dataSet = dataSet
        self.feature = -1
        self.value = 999
        self.gini = 1
        
    def split(self):
        ranges = getRanges(self.dataSet)
        range_min = ranges[0]
        range_max = ranges[1]
        intervals = 100
        giniScores = []
        for f in range(0, len(self.dataSet[0])):
            for i in range(0,intervals):
                splitFeature = f
                splitValue = range_min[f] + i*(range_max[f] - range_min[f])/1000
                subsets = getSubsets(self.dataSet, splitFeature, splitValue)
                if hasEmptySets(subsets):
                    gini = 1 #no empty sets please!
                else:
                    gini = random.uniform(0,1) #gini index is random for now!
                giniScores.append([splitFeature, splitValue, gini])        
        gini_min_id = 0
        gini_min = giniScores[0][2]
        for g in range(0, len(giniScores)):
            if giniScores[g][2] < gini_min:
                gini_min_id = g
                gini_min = giniScores[g][2]
        #print("gini_min_id",gini_min_id,"gini_min",giniScores[gini_min_id])
        self.feature = giniScores[gini_min_id][0]
        self.value = giniScores[gini_min_id][1]
        self.gini = giniScores[gini_min_id][2]
        
        
def getSubsets(dataSet, splitFeature, splitValue):    
    subset1 = []
    subset2 = []
    for x in range(0, len(dataSet)):
        if(dataSet[x][splitFeature] < splitValue):
            subset1.append(dataSet[x])
        else:
            subset2.append(dataSet[x])
    return [subset1,subset2]  

def hasEmptySets(subsets):
    for s in subsets:
        if(len(s) == 0):
            return True
    return False  

#MAIN PROGRAM
print("running!")

for i in range(0, 10): 
    print("Tree",i+1)      
    tree = Tree()
    tree.printTree()
    print("\n")
    #tree.printSubsets()   

print("done!")


