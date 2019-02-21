# -*- coding: utf-8 -*-
"""
DECISION TREE 2.0

Created on Wed Jan 16 08:01:45 2019

@author: Samson
"""
import pandas as pd
from operator import itemgetter
from tkinter import *  

FRAME_WIDTH = 1200
FRAME_HEIGHT = 800
operators = ['==','<','>']

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
targetIndex = 4
targetCategories = [0,1]
f=1.1

def class_counts(rows):
    """Counts the number of each type of example in a dataset."""
    counts = {}  # a dictionary of label -> count.
    for row in rows:
        # in our dataset format, the label is always the last column
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts

# This is the Leaf class
class Leaf:
    # This is the constructor
    def __init__(self, rows):
        #print("I am a cute little Leaf!")
        self.rows = rows
        self.predictions = class_counts(rows)
    # This prints the data corresponding with this Leaf
    def printMe(self):
        print("Leaf :", self.rows)
    # This draws the Leaf on the canvas
    def drawMe(self, drawX, drawY, size, index, layer, canvas):            
        recColor = 'green' 
        x = drawX - ((2**(layer)/2)-index-0.5)*size*f
        y = drawY + (layer)*size*f     
        canvas.create_oval(x - size/2, y + size/2, 
                                x + size/2, y - size/2,
                                fill = recColor)
# This is the Node class
class Node:
    # This is the constructor
    def __init__(self, question, trueBranch, falseBranch):
        #print("I am a cute little Node!")
        self.question = question
        self.trueBranch = trueBranch
        self.falseBranch = falseBranch
    # This prints the Node's question and continues down the tree to do the same
    # for all of it's child nodes
    def printMe(self):
        print("Node: " + self.question.text())
        self.trueBranch.printMe()
        self.falseBranch.printMe()
    # This draws the Node and all of it's child nodes on the canvas
    def drawMe(self, drawX, drawY, size, index, layer, canvas):            
        recColor = 'brown'
        x = drawX - ((2**(layer)/2)-index-0.5)*size*f
        y = drawY + (layer)*size*f  
        trueX = drawX - (2**(layer+1)/2 - 2*index-0.5)*size*f
        trueY = drawY + (layer+1)*size*f
        falseX = drawX - (2**(layer+1)/2 - (2*index+1)-0.5)*size*f
        falseY = trueY
        canvas.create_line(x, y, trueX, trueY,
                                fill = 'black')
        canvas.create_line(x, y, falseX, falseY,
                                fill = 'black')
        canvas.create_rectangle(x - size/2, y + size/2, x + size/2, y - size/2,
                                fill = recColor)
        self.trueBranch.drawMe(drawX, drawY, size, index*2, layer + 1, canvas)
        self.falseBranch.drawMe(drawX, drawY, size, index*2 + 1, layer + 1, canvas)
    #def classify(self, rows):        

# This class saves the splitcondition            
class Question:
    def __init__(self, operator, valueIndex, splitValue):
        self.operator = operator
        self.valueIndex = valueIndex
        self.splitValue = splitValue
    # This returns the splitcondition as a question in string format
    def text(self):
        return (data.columns[self.valueIndex] + ' ' + self.operator 
                + ' ' + str(self.splitValue) + "?")

# This builds the tree, returns the highest Node with all of its children
def buildTree(rows):
    info, question = findBestSplit(targetCategories, targetIndex, rows)
    #print("buildTree(",rows,"): info = " + str(info) + ", question = " + question.text())
    if info == 0 or question == None: return Leaf(rows)
    trueRows, falseRows = getSubsets(rows, question)
    trueBranch = buildTree(trueRows)
    falseBranch = buildTree(falseRows)
    return Node(question, trueBranch, falseBranch)

# This finds the best split based on the gini index
def findBestSplit(targetCategories, targetVariable, rows): 
    bestGain = None
    bestQuestion = None
    stepAmount = 10
    for operator in operators:
        for variableIndex in range(0, len(rows[0])):            
            if not (variableIndex == targetIndex):
                interval = getInterval(rows, variableIndex)
                varRange = interval[1] - interval[0]
                for x in range(0, stepAmount):
                    value = interval[0] + (varRange/stepAmount) * x                    
                    question = Question(operator, variableIndex, value)
                    if not hasEmptySets(getSubsets(rows, question)):
                        gain = infoGain(targetCategories, targetVariable, rows, question)
                        if bestGain == None:                        
                            bestGain = gain
                            bestQuestion = question
                            
                        elif gain > bestGain:                        
                            bestGain = gain
                            bestQuestion = question 
    return bestGain, bestQuestion

# This checks whether a row is a positive or negative on the split question
def answer(question, row):    
    operator = question.operator
    switcher = {
        '<': smallerThan,
        '>': biggerThan,
        '==': equalTo,   
    }
    func = switcher.get(operator, lambda: "Invalid input")
    return func(row[question.valueIndex], question.splitValue) 

def smallerThan(a, b):
    if(a < b):
        return True
    return False

def biggerThan(a,b):
    if(a > b):
        return True
    return False

def equalTo(a, b):
    if(a == b):
        return True
    return False

# This calculates the gini index for a single set
def giniIndex(targetCategories, targetVariable, rows):  
    categories = []
    for c in targetCategories:
        categories.append([])
    for row in rows:
        for c in targetCategories:
            if(row[targetVariable] == c):
                categories[c].append(row)           
    blob = 0
    for c in range (0, len(categories)):
        blob+=(len(categories[c])/len(rows))**2
    gini = 1 - blob   
    return gini   

# This calculates the weighted gini index for a set of sets
# That means it calculates the weighted (by size) average
def weightedGini(targetCategories, targetVariable, subsets):
    totalLength = 0
    for subset in subsets:
        totalLength += len(subset)
    weightedSum = 0
    for subset in subsets:
        subGini = giniIndex(targetCategories, targetVariable, subset)   
        weightedSum += subGini * len(subset)/totalLength
    return weightedSum  

#This calculates the information gain that results from the splitting of a set
#Based on a certain splitcondition (question)
def infoGain(targetCategories, targetVariable, rows, question):    
    gini1 = giniIndex(targetCategories, targetVariable, rows)
    gini2 = weightedGini(targetCategories, targetVariable, getSubsets(rows, question))
    return (gini1 - gini2)   

# This splits the rows based on the splitcondition and returns the resulting sets
def getSubsets(rows, question):
    subsets = []
    for s in range(0,2):
        subsets.append([])
    for row in rows:
        if answer(question, row):
            subsets[0].append(row)
        else:
            subsets[1].append(row)  
    return subsets

# Checks whether or not a set contains empty subsets
def hasEmptySets(subsets):
    for s in subsets:
        if(len(s) == 0):
            return True
    return False 

# Gets the interval (range) for a certain row
def getInterval(rows, index):
    minValue = rows[0][index]
    maxValue = rows[0][index]
    for row in rows:
        if row[index] < minValue:
            minValue = row[index]
        elif row[index] > maxValue:
            maxValue = row[index]
    return minValue, maxValue

def print_tree(node, spacing=""):
    """World's most elegant tree printing function."""

    # Base case: we've reached a leaf
    if isinstance(node, Leaf):
        print (spacing + "Predict", node.predictions)
        return

    # Print the question at this node
    print(spacing + node.question.text())

    # Call this function recursively on the true branch
    print (spacing + '--> True:')
    print_tree(node.trueBranch, spacing + "  ")

    # Call this function recursively on the false branch
    print (spacing + '--> False:')
    print_tree(node.falseBranch, spacing + "  ")

#MAIN PROGRAM
print("running!")
print("Data head:")
print(data.head())
print("\n")

tree = buildTree(data.values)
print_tree(tree)
"""
window = Tk()
window.title("Tree of Wisdom")

canvas = Canvas(window ,width=FRAME_WIDTH ,height=FRAME_HEIGHT)
canvas.pack()
size = FRAME_WIDTH/20
tree.drawMe(FRAME_WIDTH/2, size, size, 0, 0, canvas)

window.mainloop()
"""

print("done!")