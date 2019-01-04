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




range_min = []
range_max = []
for f in range(0, len(raw_data[0])): #for every feature
    range_min.append(raw_data[0][f]) #add the first value of the feature to the range_min list
    range_max.append(raw_data[0][f]) #add the first value of the feature to the range_max list
    for x in range(0, len(raw_data)): #for every data point
        if(raw_data[x][f] < range_min[f]): #if current value of feature smaller then the min
            range_min[f] = raw_data[x][f] #update the min
        if(raw_data[x][f] > range_max[f]): #if current value of feature bigger then the max
            range_max[f] = raw_data[x][f] #update the max

def printDataStats():    
    print(data.columns)
    print("len(raw_data) =",len(raw_data))
    print("len(raw_data)[0] =",len(raw_data[0]))
    for x in range(0,len(range_min)):
        print("feature",x, ", min=","{:.2f}".format(range_min[x]), ", max=","{:.2f}".format(range_max[x]))
    print(raw_data)
    for x in range(0,10):
        for y in range(0, len(raw_data[0])):
            print("{:.2f}".format(raw_data[x][y]), ", ", end="")
        print("\n")

class Tree:
    def __init__(self):
        self.name = "Tree"
        self.nodes = []      
        self.depth = 1
        maxDepth = 4
        index = 0        
        parentNode = Node(index, self.depth)  
        index+=1        
        self.nodes.append(parentNode)
        while(self.depth < maxDepth):
            for x in range(0, len(self.nodes)):
                if(self.nodes[x].layer == self.depth):
                    child1 = Node(index, self.depth+1)
                    index+=1
                    child2 = Node(index, self.depth+1)
                    index+=1
                    self.nodes.append(child1)
                    self.nodes.append(child2)
            self.depth+=1        
    def printTree(self):        
        for layer in range(1, self.depth + 1):
            for node in self.nodes:
                if(node.layer == layer):
                    print(node.name,", ", end="")
            print("\n")
            

class Node:
    def __init__(self, index, layer):
        self.name = "Node" + str(index)
        self.layer = layer
        self.feature = random.randint(0,len(data.columns) - 1)
        
tree = Tree()
tree.printTree()
#printDataStats()

"""

"""