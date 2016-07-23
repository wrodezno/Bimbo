# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 17:05:05 2016

@author: wrodezno
"""

import os 
os.chdir("/home/wrodezno/Documents/Bimbo/Code")
from subFun.exploreData import exploreData
from subFun.getModelTrData import getModelTrData
from subFun.getModelTestData import getModelTestData
from subFun.GetData import GetData

#%%
#EDA
exploreData()

#%%
#Set data ready for model fitting


#Get Train Data. And split to get validation and training set.  Train and Validation will be seperated by week days
getData = GetData()
trainData = getData.getDemandData(testCase = True,sample = False,fileName = '',weeks = '',myLimit = '',cust = False, custName = '')
valData  = getData.getDemandData(testCase = True,sample = False,fileName = '',weeks = '',myLimit = '',cust = False, custName = '')


#%%
#Get model data that will go into models 
modelTrData = getModelTrData(trainData)
modelValData = getModelTestData(modelTrData,valData)




#%%
#Fitting XG boost 

import xgboost 
































