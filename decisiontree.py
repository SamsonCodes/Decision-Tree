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
    print(data.columns)
    print("len(dataSet) =",len(dataSet))
    print("len(dataSet)[0] =",len(dataSet[0]))
    ranges = getRanges(dataSet)
    range_min = ranges[0]
    range_max = ranges[1]
    for x in range(0,len(range_min)):
        print("feature",x, ", min=","{:.2f}".format(range_min[x]), ", max=","{:.2f}".format(range_max[x]))
    #print(dataSet)
    """
    for x in range(0,10):
        for y in range(0, len(dataSet[0])):
            print("{:.2f}".format(dataSet[x][y]), ", ", end="")
        print("\n")
        """
    print("\n")

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
            for x in range(0, len(self.nodes)):
                if(self.nodes[x].layer == self.depth):
                    subsets = getSubsets(self.nodes[x].dataSet, self.nodes[x].feature, self.nodes[x].value)
                    child1 = Node(index, self.depth+1, subsets[0])
                    index+=1
                    child2 = Node(index, self.depth+1, subsets[1])
                    index+=1
                    self.nodes.append(child1)
                    self.nodes.append(child2)
            self.depth+=1        
    def printTree(self):        
        for layer in range(1, self.depth + 1):
            for node in self.nodes:
                if(node.layer == layer):
                    #print(node.name,", ",node.feature,", ",node.value,", ", end="")
                    print("||",node.name,":",data.columns[node.feature],"<",node.value,"||", end = "")
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
        
        ranges = getRanges(dataSet)
        range_min = ranges[0]
        range_max = ranges[1]
        
        splitFeature = random.randint(0,len(data.columns) - 1)
        splitValue = random.uniform(range_min[splitFeature], range_max[splitFeature])
        
        self.feature = splitFeature
        self.value = splitValue
        
def getSubsets(dataSet, splitFeature, splitValue):    
    subset1 = []
    subset2 = []
    for x in range(0, len(dataSet)):
        if(dataSet[x][splitFeature] < splitValue):
            subset1.append(dataSet[x])
        else:
            subset2.append(dataSet[x])
    return [subset1,subset2]    
        
tree = Tree()
tree.printTree()
tree.printSubsets()
printDataStats(raw_data)


