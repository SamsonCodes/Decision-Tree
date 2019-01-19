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

class Leaf:
    def __init__(self, rows):
        print("I am a cute little Leaf!")
        self.rows = rows
    def printMe(self):
        print("Leaf :", self.rows)
    def drawMe(self, drawX, drawY, size, layer, canvas):            
        recColor = 'green'  
        canvas.create_oval(drawX - size/2, drawY + size/2, 
                                drawX + size/2, drawY - size/2,
                                fill = recColor)
class Node:
    def __init__(self, question, trueBranch, falseBranch):
        print("I am a cute little Node!")
        self.question = question
        self.trueBranch = trueBranch
        self.falseBranch = falseBranch
    def printMe(self):
        print("Node: " + self.question.text())
        self.trueBranch.printMe()
        self.falseBranch.printMe()
    def drawMe(self, drawX, drawY, size, layer, canvas):            
        recColor = 'brown'  
        trueX = drawX - size/1.8 - layer*size/1.8
        trueY = drawY + size*1.1
        falseX = drawX + size/1.8 + layer*size/1.8
        falseY = trueY
        canvas.create_line(drawX, drawY, trueX, trueY,
                                fill = 'black')
        canvas.create_line(drawX, drawY, falseX, falseY,
                                fill = 'black')
        canvas.create_rectangle(drawX - size/2, drawY + size/2, 
                                drawX + size/2, drawY - size/2,
                                fill = recColor)
        self.trueBranch.drawMe(trueX, trueY, size, layer + 1, canvas)
        self.falseBranch.drawMe(falseX, falseY, size, layer + 1, canvas)
            
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
tree.printMe()

window = Tk()
window.title("Tree of Wisdom")

canvas = Canvas(window ,width=FRAME_WIDTH ,height=FRAME_HEIGHT)
canvas.pack()
size = FRAME_WIDTH/20
tree.drawMe(FRAME_WIDTH/2, size/2.2, size, 0, canvas)

window.mainloop()


print("done!")