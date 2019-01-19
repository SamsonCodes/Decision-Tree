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

ABC = [[0,0,0],[0,1,0],[1,0,0],[1,1,1]]
data = pd.DataFrame(data = ABC, columns = ["A","B","C"], copy = False)
targetCategories = [0, 1]
stepAmount = 10
targetIndex = 2

class Leaf:
    def __init__(self, rows):
        print("I am a cute little Leaf!")
        self.rows = rows
    def printLeaf(self):
        print("Leaf :", self.rows)

class Node:
    def __init__(self, question, trueBranch, falseBranch):
        print("I am a cute little Node!")
        self.question = question
        self.trueBranch = trueBranch
        self.falseBranch = falseBranch
    def printNode(self):
        print("Node: " + self.question.text())
        if(isinstance(self.trueBranch, Node)):
            self.trueBranch.printNode()
        else:
            self.trueBranch.printLeaf()
        if(isinstance(self.falseBranch, Node)):
            self.falseBranch.printNode()
        else:
            self.falseBranch.printLeaf()
        
        
        
class Question:
    def __init__(self, operator, valueIndex, splitValue):
        self.operator = operator
        self.valueIndex = valueIndex
        self.splitValue = splitValue
    def text(self):
        return (data.columns[self.valueIndex] + ' ' + self.operator 
                + ' ' + str(self.splitValue) + "?")

def buildTree(rows):
    info, question = findBestSplit(targetCategories, targetIndex, rows)
    #print("buildTree(",rows,"): info = " + str(info) + ", question = " + question.text())
    if info == 0 or question == None: return Leaf(rows)
    trueRows, falseRows = getSubsets(rows, question)
    trueBranch = buildTree(trueRows)
    falseBranch = buildTree(falseRows)
    return Node(question, trueBranch, falseBranch)

def findBestSplit(targetCategories, targetVariable, rows): 
    bestGain = None
    bestQuestion = None
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

def weightedGini(targetCategories, targetVariable, subsets):
    totalLength = 0
    for subset in subsets:
        totalLength += len(subset)
    weightedSum = 0
    for subset in subsets:
        subGini = giniIndex(targetCategories, targetVariable, subset)   
        weightedSum += subGini * len(subset)/totalLength
    return weightedSum  

def infoGain(targetCategories, targetVariable, rows, question):    
    gini1 = giniIndex(targetCategories, targetVariable, rows)
    gini2 = weightedGini(targetCategories, targetVariable, getSubsets(rows, question))
    return (gini1 - gini2)   

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

def hasEmptySets(subsets):
    for s in subsets:
        if(len(s) == 0):
            return True
    return False 

def getInterval(rows, index):
    minValue = rows[0][index]
    maxValue = rows[0][index]
    for row in rows:
        if row[index] < minValue:
            minValue = row[index]
        elif row[index] > maxValue:
            maxValue = row[index]
    return minValue, maxValue

#MAIN PROGRAM
print("running!")
print("Data head:")
print(data.head())
print("\n")

tree = buildTree(data.values)
tree.printNode()
"""
window = Tk()
window.title("Tree of Wisdom")

canvas = Canvas(window ,width=FRAME_WIDTH ,height=FRAME_HEIGHT)
canvas.pack()

window.mainloop()
"""

print("done!")