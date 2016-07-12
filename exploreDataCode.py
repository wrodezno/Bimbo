"""
Spyder Editor

This is a temporary script file.
Purpose: To explore data through plotting.
         
"""


#Importing libraries we need 
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
import subFunctions.getProductTable as getProductTable
#%%
#Loading data

locationTableLoc = "/home/wrodezno/Documents/Bimbo/Data/town_state.csv"
demandDataLoc = "/home/wrodezno/Documents/Bimbo/Data/codeTestData.csv"
demandCol =['Semana','Agencia_ID','Canal_ID','Ruta_SAK','Cliente_ID','Producto_ID','Venta_uni_hoy',\
'Venta_hoy','Dev_uni_proxima','Dev_proxima','Demanda_uni_equil']

productTable = getProductTable.getProductTable()
clientData = getProductTable.getClientData()
demandData = pd.read_csv(demandDataLoc,names = demandCol)

locData = pd.read_csv(locationTableLoc)


#%%
#Customer ID Investigation 

#Histogram of customer ids
clientData.Cliente_ID = clientData.Cliente_ID.astype('int64')
f, ax = plt.subplots(figsize=(20, 3))
maxBound = 10000000
jumps = 500000
myBounds = range(0,maxBound,jumps)
myBounds.append(np.inf)
myXTicks = range(0,maxBound+jumps,jumps)
sns.set_style("whitegrid")
ax = sns.distplot(clientData.Cliente_ID,kde = False,rug = False,hist = True,bins = myBounds,ax=ax)
ax.set_xticks(myXTicks)
ax.set_xlim((0,maxBound))
#ax.set_ylim((0,100))
#%%
#brand vs Demand
#demandBrandTable



brandDemand = pd.merge(demandData, productTable.loc[:,('Producto_ID','Brands')], how='left', on=['Producto_ID','Producto_ID'])































