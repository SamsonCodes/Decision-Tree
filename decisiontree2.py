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
operators = ['>','<','==']

ABC = [[0,0,0],[0,1,0],[1,0,0],[1,1,1]]
data = pd.DataFrame(data = ABC, columns = ["A","B","C"], copy = False)
targetIndex = 2

class Node:
    def __init__(self, question, trueBranch, falseBranch):
        self.question = question
        self.trueBranch = trueBranch
        self.falseBranch = falseBranch
        print(self.question.text(data[0]))

class Leaf:
    def __init__(self, rows):
        self.rows = rows
        
class Question:
    def __init__(self, operator, valueIndex, splitValue):
        self.operator = operator
        self.valueIndex = valueIndex
        self.splitValue = splitValue
    def text(self):
        return ("Is " + data.columns[self.valueIndex] + self.operator 
                + str(self.splitValue) + "?")

def buildTree(rows):
    info, question = findBestSplit(rows)
    return Node(question, 0, 0)

def findBestSplit(rows):  
    info = 0
    question = Question(operators[0], 0, 0)
    return info, question

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

def answer(question, row):    
    operator = question.operator
    switcher = {
        '<': smallerThan,
        '>': biggerThan,
        '==': equalTo,   
    }
    func = switcher.get(operator, lambda: "Invalid month")
    return func(row[question.valueIndex], question.splitValue) 

def giniIndex(targetCategories, targetVariable, dataSet):  
    categories = []
    for c in targetCategories:
        categories.append([])
    for row in dataSet:
        for c in targetCategories:
            if(row[targetVariable] == c):
                categories[c].append(row)           
    blob = 0
    for c in range (0, len(categories)):
        blob+=(len(categories[c])/len(dataSet))**2
    gini = 1 - blob   
    return gini      
    

#MAIN PROGRAM
print("running!")
print("Data head:")
print(data.head())
print("\n")

print("Gini = " + str(giniIndex([0,1],2,data.values[3:4])))

window = Tk()
window.title("Tree of Wisdom")

canvas = Canvas(window ,width=FRAME_WIDTH ,height=FRAME_HEIGHT)
canvas.pack()

window.mainloop()

print("done!")