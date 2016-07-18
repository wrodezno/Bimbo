# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 18:36:17 2016

@author: wrodezno
"""
import os 
os.chdir('/home/wrodezno/Documents/Bimbo/Code')
import pandas as pd 
import xgboost as xgb
import sklearn as sk
import numpy as np
import scipy as sp
import subFunctions.getProductTable as getProductTable



#%%
#Load Dummy Data 
dataLoc = '/home/wrodezno/Documents/Bimbo/Data/codeTestData.csv'
demandCol =['Semana','Agencia_ID','Canal_ID','Ruta_SAK','Cliente_ID','Producto_ID','Venta_uni_hoy',\
'Venta_hoy','Dev_uni_proxima','Dev_proxima','Demanda_uni_equil']
trainData = pd.read_csv(dataLoc,names = demandCol)
trainData = trainData.loc[1:10000,:]



#%%
#Functions used throught 

def getmyGetDummyVar(x,dataFrame,**kwargs):
    tempSeries = pd.get_dummies(dataFrame[x],**kwargs)
    del dataFrame[x]
    return pd.concat([dataFrame,tempSeries])
    
#%%
#Parsing data to get it ready for model fitting 
clientData = getProductTable.getClientData()
locData = getProductTable.getLocData()
productTable = getProductTable.getProductTable()

#%%

#Mergeing the Product Data to the train data 
colIndex = range(0,48)
colIndex[1] = []
colIndex[4] = []
trainData = pd.merge(trainData, productTable.ix[:,colIndex], how='left', on=['Producto_ID'],sort=False)



#Merging the location data to the train data
trainData = pd.merge(trainData, locData.loc[:,('Agencia_ID','Town','State')], how='left', on=['Agencia_ID'],sort=False)



#%%
#Creating Dummy Variables


#%%
#Canal Data
col = 'Canal_ID'
myPrefix= 'Canal'
trainData = getmyGetDummyVar(col,trainData,prefix = myPrefix,dummy_na = True)
#%%
# Agencia Dummy Variable
col = 'Agencia_ID'
myPrefix= 'Agencia'
trainData = getmyGetDummyVar(col,trainData,prefix = myPrefix,dummy_na = True)

#%%
# Ruta_SAK Dummy Variable
col = 'Ruta_SAK'
myPrefix= 'Ruta_SAK'
trainData = getmyGetDummyVar(col,trainData,prefix = myPrefix,dummy_na = True)
#%%

# Town Dummy Variable
col = 'Town'
myPrefix= 'Town'
trainData = getmyGetDummyVar(col,trainData,prefix = myPrefix,dummy_na = True)


#%%
# State Dummy Variable
col = 'State'
myPrefix= 'State'
trainData = getmyGetDummyVar(col,trainData,prefix = myPrefix,dummy_na = True)

#%%

# Brands Dummy Variable
col = 'Brands'
myPrefix= 'Brand'
trainData = getmyGetDummyVar(col,trainData,prefix = myPrefix,dummy_na = True)




#%%
#Fitting model 














