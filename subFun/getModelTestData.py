# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 19:56:32 2016

@author: wrodezno
"""

#The purpose of this code is to get parsed test data


#%%
def getModelTestData(modelTrData,test):

    treeVar = modelTrData.columns.str.contains('_mean')
    col = modelTrData.columns[treeVar]
    for c in col:
        test[c] = modelTrData[c]
        
    return test

    
    








