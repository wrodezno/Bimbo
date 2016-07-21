# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 18:36:17 2016

@author: wrodezno
"""
import os 
os.chdir('/home/wrodezno/Documents/Bimbo/Code')
import pandas as pd 
import sklearn as sk
import numpy as np
import scipy as sp
import subFunctions.getProductTable as getProductTable

#%%
#Load train Data 
trainDataLoc= '/home/wrodezno/Documents/Bimbo/Data/sampleTrainData_weeks_3_4_5_6_07_18_2016_00_25_55.pkl'
trainData = pd.read_pickle(trainDataLoc)
trainFlag = trainData.Semana.isin([3])
trainData =  trainData.loc[trainFlag,:]
trainData = trainData.loc[:30000,('Semana','Agencia_ID','Canal_ID','Ruta_SAK','Cliente_ID','Producto_ID','Demanda_uni_equil')]
#%%
#Functions used throught 

def getmyGetDummyVar(x,dataFrame,**kwargs):
    tempSeries = pd.get_dummies(dataFrame[x],**kwargs)
    del dataFrame[x]
    return pd.concat([dataFrame,tempSeries],axis = 1)
    
#%%
#Parsing data to get it ready for model fitting 
clientData = getProductTable.getClientData()
locData = getProductTable.getLocData()
productTable = getProductTable.getProductTable()

#%%

#Mergeing the Product Data to the train data 
colIndex = range(0,48)
del colIndex[1]
del colIndex[3]
colIndex = set(colIndex)
trainData = pd.merge(trainData, productTable.ix[:,colIndex], how='left', on=['Producto_ID'],sort=False)
#Merging the location data to the train data
trainData = pd.merge(trainData, locData.loc[:,('Agencia_ID','Town','State')], how='left', on=['Agencia_ID'],sort=False)

#%%
#Creating Dummy Variables


#%%
#Canal Data
col = 'Canal_ID'
myPrefix= 'Canal'
trainData = getmyGetDummyVar(col,trainData,prefix = myPrefix)

https://mail.google.com/mail/u/0/#inbox
#%%
# Agencia Dummy Variable
col = 'Agencia_ID'
myPrefix= 'Agencia'
trainData = getmyGetDummyVar(col,trainData,prefix = myPrefix)

#%%
# Ruta_SAK Dummy Variable
#col = 'Ruta_SAK'
#myPrefix= 'Ruta_SAK'
#trainData = getmyGetDummyVar(col,trainData,prefix = myPrefix)
#%%

# Town Dummy Variable
col = 'Town'
myPrefix= 'Town'
trainData = getmyGetDummyVar(col,trainData,prefix = myPrefix)


#%%
# State Dummy Variable
col = 'State'
myPrefix= 'State'
trainData = getmyGetDummyVar(col,trainData,prefix = myPrefix)

#%%import xgboost as xgb


# Brands Dummy Variable
col = 'Brands'
myPrefix= 'Brand'
trainData = getmyGetDummyVar(col,trainData,prefix = myPrefix)


#%%

#%%
#Fitting model 
#%%

#Using R functions 

#%%
#Training XBboost 

del trainData['Ruta_SAK']


trainData.to_csv('/home/wrodezno/Documents/Bimbo/Data/trainR.csv')


#%%
















































