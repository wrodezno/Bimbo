# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 18:36:17 2016

@author: wrodezno
"""
#%%
#Functions used throught 
def getModelTrData(modelData):
    import os 
    os.chdir('/home/wrodezno/Documents/Bimbo/Code')
    import pandas as pd 
    from subFun.GetData import GetData

#%%    
    #Functions used throug out the code
    def getmyGetDummyVar(x,dataFrame,**kwargs):
        tempSeries = pd.get_dummies(dataFrame[x],**kwargs)
        del dataFrame[x]
        return pd.concat([dataFrame,tempSeries],axis = 1)
        
       
       
    def repCatMean(x,dataFrame):
        new_x = '_'.join([x,'_mean'])
        grpData = dataFrame.loc[:,('Demanda_uni_equil',x)].groupby([x]).mean()
        grpData[x] = grpData.index
        dummyData = pd.merge(dataFrame, grpData, how='left', on=[x],sort=False)
        modelData[new_x] = dummyData['Demanda_uni_equil_y']
        return modelData
    
    #%%
    #Parsing data to get it ready for model fitting 
    getData = GetData()
    #clientData = getData.getClientData()
    locData = getData.getLocData()
    productData = getData.getProductData()    
    #%%
    modelData = modelData.loc[:,('Semana','Agencia_ID','Canal_ID','Ruta_SAK','Cliente_ID','Producto_ID','Demanda_uni_equil')]
    
    #%%
    
    #Mergeing the Product Data to the train data 
    prodColNames = productData.columns
    #prodColNames = prodColNames.drop('Producto_ID')
    prodColNames = prodColNames.drop('prodWeightRaw')    
    modelData = pd.merge(modelData, productData.ix[:,prodColNames], how='left', on=['Producto_ID'],sort=False)
    #Merging the location data to the train data
    modelData = pd.merge(modelData, locData.loc[:,('Agencia_ID','Town','State')], how='left', on=['Agencia_ID'],sort=False)
    #%%
    #Handling Categorical Data
    
    #%%
    #Morphing Categorical data for regression trees
    col = ['Canal_ID','Agencia_ID','Town','State','Brands','Ruta_SAK','Producto_ID','questionName']
    cnt = 1
    for c in col:  
        print 'Getting Data to put into models'
        print str(cnt) + ' of ' + str(len(col))
        modelData = repCatMean(c,modelData)
        cnt+=1
    #%%        
        
    return modelData
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
