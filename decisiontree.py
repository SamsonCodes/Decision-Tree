# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 10:24:24 2019

@author: Samson
"""
import random
import pandas as pd
from operator import itemgetter
from tkinter import *  

FRAME_WIDTH = 1200
FRAME_HEIGHT = 800
BOX_WIDTH = 120

"""
ABC = [[0,0,0],[0,1,0],[1,0,0],[1,1,1]]
data = pd.DataFrame(data = ABC, columns = ["A","B","C"], copy = False)
targetVariable = 2
targetCategories = [0,1]
"""

"""
Golf = [[0,2,1,0,0],
        [0,2,1,1,0],
        [1,2,1,0,1],
        [2,1,1,0,1],
        [2,0,0,0,1],
        [2,0,0,1,0],
        [1,0,0,1,1],
        [0,1,1,0,0],
        [0,0,0,0,1],
        [2,1,0,0,0],
        [0,1,0,1,1],
        [1,1,1,1,1],
        [1,2,0,0,1],
        [2,1,1,1,0]]
data = pd.DataFrame(data = Golf, columns = ["Outlook","Temp","Humidity","Windy","Play"], copy = False)
targetVariable = 4
targetCategories = [0,1]
"""

dataset_url = 'http://mlr.cs.umass.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv'
data = pd.read_csv(dataset_url, sep=';')
targetVariable = 11
targetCategories = []
intervalSteps = 5 

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
        maxDepth = 10
        index = 0          
        parentNode = Node(index, self.depth, raw_data)  
        index+=1        
        self.nodes.append(parentNode)
        while(self.depth < maxDepth):
            #print("self.depth=",self.depth, "len(self.nodes)=",len(self.nodes))
            for x in range(0, len(self.nodes)):
                #print("x=",x,",len(self.nodes[x].dataSet)=",len(self.nodes[x].dataSet))
                if(self.nodes[x].layer == self.depth):    
                    if(len(self.nodes[x].dataSet) >= 2 and not self.nodes[x].leaf):
                        self.nodes[x].split()
                        subsets = getSubsets(self.nodes[x].dataSet, self.nodes[x].feature, self.nodes[x].value)
                        if not (hasEmptySets(subsets)):
                            child1 = Node(index, self.depth+1, subsets[0])                            
                            self.nodes[x].addChild(index)
                            index+=1
                            self.nodes.append(child1)
                            child2 = Node(index, self.depth+1, subsets[1])
                            self.nodes[x].addChild(index)
                            index+=1
                            self.nodes.append(child2) 
            self.depth+=1        
    def printTree(self):        
        for layer in range(1, self.depth + 1):
            for node in self.nodes:
                if(node.layer == layer):
                    if not node.leaf:
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
    def draw(self, canvas):
        for layer in range(1, self.depth + 1): 
            layerNodes = []
            for node in self.nodes:                
                if(node.layer == layer):    
                    layerNodes.append(node)
            for n in range (0, len(layerNodes)):                
                x = FRAME_WIDTH * (n + 1) / (1 + len(layerNodes))                    
                recWidth = BOX_WIDTH
                recHeight = 70
                if not layerNodes[n].leaf:                        
                    lines = [layerNodes[n].name, str(data.columns[layerNodes[n].feature]) + "<" + "{:.2f}".format(layerNodes[n].value),"gini =" + "{:.2f}".format(layerNodes[n].gini),"data set size =" + str(len(layerNodes[n].dataSet))]
                else:
                    lines = [layerNodes[n].name, "category =" + str(layerNodes[n].category), "data set size =" + str(len(layerNodes[n].dataSet))]
                layerNodes[n].draw(x - recWidth/2,layer*recHeight*1.1 - recHeight/2,recWidth, recHeight, lines, canvas)
    def whatIsThis(self, dataRow):
        currentId = 0
        if(dataRow[self.nodes[0].feature] < self.nodes[0].value):
            currentId = 1
        else:
            currentId = 2
        stop = False
        loops = 0
        while ((not self.nodes[currentId].leaf) and (not stop) and (loops < 1000)):
            loops+=1
            if len(self.nodes[currentId].children) == 0:
                stop = True
                print("stop = True")
            else:
                if(dataRow[self.nodes[currentId].feature] < self.nodes[currentId].value):
                    currentId = self.nodes[currentId].children[0]
                else:
                    currentId = self.nodes[currentId].children[1]
        if self.nodes[currentId].leaf:
            print(dataRow,"-->",self.nodes[currentId].category)  
        
class Node:
    def __init__(self, index, layer, dataSet):
        firstRowCategory = getCategory(dataSet[0][targetVariable]) #used in the for loop to determine whether or not the dataset is pure       
        self.leaf = True #Leaf until proven otherwise
        #print("node",index,", firstRowCategory =",firstRowCategory) 
        #print("dataSet=",dataSet)
        for row in dataSet:            
            if(getCategory(row[targetVariable]) != firstRowCategory): #if the data set is not pure
                #if(self.leaf):
                    #print(row[targetVariable],"category=",getCategory(row[targetVariable]))
                    #print("Not a leaf this is!")
                self.leaf = False #then this node is not a leaf
        
        if(self.leaf):
            self.name = "Leaf" + str(index)
            self.category = firstRowCategory
        else:            
            self.name = "Node" + str(index)
        self.index = index
        print("classified as",self.name)
        self.layer = layer      
        self.dataSet = dataSet
        self.feature = -1
        self.value = 999
        self.gini = 0
        self.children = []
    def draw(self, drawX, drawY, recWidth, recHeight, lines, canvas):
        if(self.leaf):
            recColor = 'darkGreen'  
            canvas.create_oval(drawX,drawY,drawX+recWidth,drawY+recHeight, fill = recColor)
            for i in range(0, len(lines)):            
                canvas.create_text(drawX + recWidth/2,drawY + 10 + i * (recHeight/len(lines)),fill="white",font="Times 8 italic bold",
                                    text=lines[i])
        else:            
            recColor = 'brown'  
            canvas.create_rectangle(drawX,drawY,drawX+recWidth,drawY+recHeight, fill = recColor)
            for i in range(0, len(lines)):            
                canvas.create_text(drawX + recWidth/2,drawY + 10 + i * (recHeight/len(lines)),fill="white",font="Times 8 italic bold",
                                    text=lines[i])
    def addChild(self,index):
        self.children.append(index)    
    def split(self):
        ranges = getRanges(self.dataSet)
        range_min = ranges[0]
        range_max = ranges[1]
        intervals = 10
        giniScores = []
        for f in range(0, len(self.dataSet[0])):
            if (f != targetVariable): # Obviously we don't want to split on our target variable
                for i in range(0,intervals):
                    splitFeature = f
                    splitValue = range_min[f] + i*(range_max[f] - range_min[f])/intervals
                    subsets = getSubsets(self.dataSet, splitFeature, splitValue)
                    if not hasEmptySets(subsets):
                        gini = giniIndex(splitFeature,splitValue,self.dataSet) #gini index is random for now!
                        giniScores.append([splitFeature, splitValue, gini])
        
        giniScores.sort(key = itemgetter(2)) #Sorts the list by gini score in ascending order
        gini_min_id = 0
        
        #print("gini_min_id",gini_min_id,"gini_min",giniScores[gini_min_id])
        self.feature = giniScores[gini_min_id][0]
        self.value = giniScores[gini_min_id][1]
        self.gini = giniScores[gini_min_id][2]

def giniIndex(feature,value,dataSet):
    subsets = getSubsets(dataSet,feature,value)
    ginis = []
    for subset in subsets:
        categories = []
        if isinstance(targetCategories[0], list):
            for interval in targetCategories:
                categories.append([])
            for row in subset:
                for interval in targetCategories:
                    if(getCategory(row[targetVariable]) == getCategory(interval[1])):
                        categories[getCategory(interval[1])].append(row)            
            blob = 0
            for c in range (0, len(categories)):
                blob+=(len(categories[c])/len(dataSet))**2
            localGini = 1 - blob
            ginis.append(localGini)
        else:
            for c in targetCategories:
                categories.append([])
            for row in subset:
                for c in targetCategories:
                    if(getCategory(row[targetVariable]) == c):
                        categories[c].append(row)           
            blob = 0
            for c in range (0, len(categories)):
                blob+=(len(categories[c])/len(dataSet))**2
            localGini = 1 - blob
            ginis.append(localGini)
    gini = 0
    for g in range(0,len(ginis)):
        gini+=(ginis[g]*len(subsets[g]))/len(dataSet)    
    return gini        
        
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

def getCategory(targetValue):
    if isinstance(targetCategories[0], list):  #If categories are intervals        
        if targetValue == targetCategories[0][0]:
                return 0     
        for interval in targetCategories:
            if targetValue > interval[0] and targetValue <= interval[1]:
                return targetCategories.index(interval) #return what interval it is in
    else: #If categories are simply values        
        return targetValue #Simply return the value

def setUp(steps):
    ranges = getRanges(raw_data)
    targetVariableInterval = [ranges[0][targetVariable],ranges[1][targetVariable]]
    print("targetVariableInterval=",targetVariableInterval)
    targetVariableRange = targetVariableInterval[1] - targetVariableInterval[0]    
    for x in range(0, steps):
        targetCategories.append([targetVariableInterval[0] + x*(targetVariableRange/steps), targetVariableInterval[0] + (x+1)*(targetVariableRange/steps)])
    print("targetCategories =",targetCategories)   


#MAIN PROGRAM
print("running!")
print("head")
print(data.head())
print("\n")
if(len(targetCategories) == 0):
    setUp(intervalSteps)

     
tree = Tree()
tree.printTree()
    #tree.printSubsets()   
"""for dataRow in raw_data:
    tree.whatIsThis(dataRow)"""
    
window = Tk()
window.title("Tree of Wisdom")

#gui.geometry(str(FRAME_WIDTH) + "x" + str(FRAME_HEIGHT))
#f1.printField()T))

canvas = Canvas(window ,width=FRAME_WIDTH ,height=FRAME_HEIGHT)
canvas.pack()
tree.draw(canvas)

window.mainloop()

print("done!")


