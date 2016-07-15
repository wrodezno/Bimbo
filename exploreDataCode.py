"""
Spyder Editor

This is a temporary script file.
Purpose: To explore data through plotting.
         
"""


#Importing libraries we need 
import seaborn as sns
import sklearn as sk
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
import subFunctions.getProductTable as getProductTable
#%%
#Functions which will be used repeatedly throughout the code 

def hbars(colrow,colcol,groupedData,tempcolors,title,ylab,xlab):
    valuePlotting = sns.barplot(x = colcol,y = colrow,order = groupedData[colcol],data = groupedData)
    fig, ax = plt.subplots()                                                       #Plot Figure and axes handles 
    fig.set_size_inches(14, 14)
    sns.despine()
    ax = sns.barplot(x = colrow,y = colcol,data = groupedData,order = groupedData[colcol], palette = tempcolors)
    plt.setp(ax.patches, linewidth=0)   
    ax.set_title(title,fontsize = 16)
    ax.set_ylabel(ylab,fontsize = 15)
    ax.set_xlabel(xlab,fontsize = 15)
    for p in valuePlotting.patches:
        xpos = p.get_height()
        height = p.get_x()   
        if xpos > 50:
            t = .01
        elif xpos > 8:
            t = .008
        elif xpos > 15:
            t = .001
        else:
            t = .1
        ax.text(xpos + t*xpos, height+ .5, '%1.1f'%(xpos))

#%%
#Loading data

histSaveLoc = "/home/wrodezno/Documents/Bimbo/Code/test.pdf"
locationTableLoc = "/home/wrodezno/Documents/Bimbo/Data/town_state.csv"
clientData = getProductTable.getClientData()
locData = pd.read_csv(locationTableLoc)
#brand vs Demand
#demandBrandTable
demandDataLoc = "/home/wrodezno/Documents/Bimbo/Data/codeTestData.csv"
demandCol =['Semana','Agencia_ID','Canal_ID','Ruta_SAK','Cliente_ID','Producto_ID','Venta_uni_hoy',\
'Venta_hoy','Dev_uni_proxima','Dev_proxima','Demanda_uni_equil']
demandData = pd.read_csv(demandDataLoc,names = demandCol)
productTable = getProductTable.getProductTable()
demandData = demandData.loc[:70000,:]


#%%
#Customer ID Investigation 

#Histogram of customer ids


pandclientData.Cliente_ID = clientData.Cliente_ID.astype('int64')
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





#Clustering the Client Ids
#clusterAlgo = sk.cluster.MiniBatchKMeans(n_clusters=4, init='k-means++', n_init=10, max_iter=300, tol=0.0001,random_state = 5)
#clusterAlgo.fit(clientData.Cliente_ID)
#clientClusters = clusterAlgo.predict(clientData.Cliente_ID)





#%%

#Demand per Brand
productDemandLinkData = pd.merge(demandData, productTable, how='left', on=['Producto_ID'],sort=True)
brandGroupedData = productDemandLinkData.groupby('Brands')
brandGroupedData = brandGroupedData['Demanda_uni_equil'].agg([np.mean, np.std,np.sum,np.median]).sort('median',ascending = True)
brandGroupedData['Brands'] = brandGroupedData.index

#Boxplot
fig, ax = plt.subplots()                                                       #Plot Figure and axes handles 
fig.set_size_inches(14, 8.27) 
sns.set_style("whitegrid")
ax = sns.boxplot(x="Brands", y="Demanda_uni_equil", data=productDemandLinkData,order = brandGroupedData['Brands'],palette = 'hls')
ax.set_xticklabels(ax.get_xticklabels(),rotation='vertical')
ax.set_ylabel('Demand',fontsize = 15)
ax.set_xlabel('Brands',fontsize = 15)
ax.set_title('Brand Demand Distribution',fontsize = 14)

#Plotting Median 
hbars('median','Brands',brandGroupedData,"hls",'Median Demand per Brand','Brands','Median Demand')


#%%
#Checking out mystery variable 


varWithData =  productDemandLinkData.ix[:,19:].sum() > 0


sortedMstyVariable = productDemandLinkData.ix[:,19:].sum()[varWithData].sort_values(ascending = True).index








boxes=[]
varMedian = []
demandVar =[]
maxDemand =[]
for var in sortedMstyVariable:   
    
    tempFlag = productDemandLinkData[var]
    tempData = productDemandLinkData['Demanda_uni_equil'][tempFlag]    
    varMedian.append(tempData.median())
    demandVar.append(np.sum(tempData))
    maxDemand.append(np.max(tempData))
    boxes.append(tempData)



#Seeting box plot variables
sindex = np.argsort(varMedian)
boxes= [boxes[i] for i in sindex]
demanvarPlot = np.array([demandVar[i] for i in sindex])
ylabels = [sortedMstyVariable[i] for i in sindex]




#Var Box Plot
fig, ax = plt.subplots()                                                       
fig.set_size_inches(14, 14)
sns.set_style("whitegrid")
bp = ax.boxplot(boxes,vert=0)
plt.setp(bp['boxes'], color='black')
plt.setp(bp['whiskers'], color='black')
mycolors = [255/float(255),127/float(255),14/float(255)]
fig, ax = plt.subplots()                                                       
fig.set_size_inches(14, 11.27)
ax = sns.boxplot(data=boxes,orient = 'h',color = mycolors)
ax.set_title('Mystery Variable Distribution',fontsize = 16)
ax.set_ylabel('Variable',fontsize = 14)
ax.set_xlabel('Demand',fontsize=14)
ax.set_xlim((-0.1,48.5))
ax.set_yticklabels(ylabels)

#Demand per mystery variable 




valuePlotting = sns.barplot(x = ylabels,y = demanvarPlot)
fig, ax = plt.subplots()                                                       #Plot Figure and axes handles 
fig.set_size_inches(14, 14)
sns.despine()
sns.set_style("whitegrid")
ax = sns.barplot(x = demanvarPlot,y = ylabels,color = mycolors)
plt.setp(ax.patches, linewidth=0)   
ax.set_title('Cumulative Demand Per Variable.  N = ' +  str(demanvarPlot.sum()),fontsize = 16)
ax.set_ylabel('Variable',fontsize = 14)
ax.set_xlabel('Demand',fontsize=14)

for p in valuePlotting.patches:
    xpos = p.get_height()
    height = p.get_x()   
    if xpos > 50:
        t = .01
    elif xpos > 8:
        t = .008
    elif xpos > 15:
        t = .001
    else:
        t = .1
    ax.text(xpos + t*xpos, height+ .5, '%1.0f'%(xpos))








#%%
#Canal ID





groupedCanalData = demandData.groupby('Canal_ID')
groupedCanalData = groupedCanalData['Demanda_uni_equil'].agg([np.mean, np.std,np.sum,np.median]).sort('median',ascending = True)
groupedCanalData['Canal_ID'] = groupedCanalData.index
groupedCanalData['Canal_ID'] =  groupedCanalData['Canal_ID'].astype('category')
fig, ax = plt.subplots()                                                       #Plot Figure and axes handles 
fig.set_size_inches(14, 8.27) 
sns.set_style("whitegrid")
ax = sns.boxplot(x="Canal_ID", y="Demanda_uni_equil", data=demandData, order = groupedCanalData.index,palette = 'hls')
#Median per group
hbars('median','Canal_ID',groupedCanalData,"Blues_d",'Median Demand per Canal','Canal_ID','Median Demand')
#%%
#Does Price have an effect on Demand?





pricePerUnit = demandData.Venta_hoy/demandData.Venta_uni_hoy
demandData['pricePerUnit'] = pricePerUnit


demandData['pricePerUnitLogged'] = np.log10(pricePerUnit)
demandData['DemandLogged'] = np.log10(demandData.Demanda_uni_equil)



#Price vs Demand Scatter Plot
fig, ax = plt.subplots()                                                       #Plot Figure and axes handles 
fig.set_size_inches(14, 8.27) 
sns.set_style("whitegrid")
ax = sns.regplot(x="pricePerUnit", y="Demanda_uni_equil", data=demandData,scatter_kws=dict(alpha=.5),fit_reg = False);   
ax.set_xlabel('Price Per Unit',fontsize = 14)
ax.set_ylabel('Number of Units Demanded',fontsize = 14)
ax.set_title('Unit Price vs Demand',fontsize = 16)
ax.set_ylim((0,np.max(demandData['Demanda_uni_equil'])))
#ax.set_xlim((0,np.max(demandData['pricePerUnit'])))
ax.set_xlim((0,50)





#Prices Logged
fig, ax = plt.subplots()                                                       #Plot Figure and axes handles 
fig.set_size_inches(14, 8.27) 
sns.set_style("whitegrid")
ax = sns.regplot(x="pricePerUnitLogged", y="DemandLogged", data=demandData,scatter_kws=dict(alpha=.5))  
#ax.set_xlim((0,200))
#ax.set_ylim((0,40))
ax.set_xlabel('Price Per Unit Logged',fontsize = 14)
ax.set_ylabel('Number of Units Demanded',fontsize = 14)
ax.set_title('Unit Price Logged vs Demand',fontsize = 16)
ax.set_ylim((0,np.max(demandData['DemandLogged'])))
ax.set_xlim((0,np.max(demandData['pricePerUnitLogged'])))



#How much do prices vary within a product.  Average price variation within produect 
productPriceTable = demandData.loc[:,('Producto_ID','pricePerUnit')]
productPriceGroupedData = productPriceTable.groupby('Producto_ID')
productPriceGroupedData = productPriceGroupedData['pricePerUnit'].agg([np.mean, np.std])
productPriceGroupedData['cv'] = 100*productPriceGroupedData['std']/productPriceGroupedData['mean']
productPriceGroupedData = productPriceGroupedData.loc[~productPriceGroupedData['cv'].isnull()]




f, ax = plt.subplots()                                                     #Plot Figure and axes handles 
fig.set_size_inches(14, 8.27) 
sns.set_style("whitegrid")
ax = sns.distplot(productPriceGroupedData['cv'],rug=True)
ax.set_xlabel('Coefficient of Variation',fontsize = 14)
ax.set_ylabel('Count',fontsize = 14)
ax.set_title('Price Coefficient of Variation per Product',fontsize = 14)


#Mean Price Distribution 
f, ax = plt.subplots()                                                     #Plot Figure and axes handles 
fig.set_size_inches(14, 8.27) 
ax = sns.distplot(productPriceGroupedData['mean'],rug=True,color = 'g')
ax.set_xlabel('Mean Price',fontsize = 14)
ax.set_ylabel('Count',fontsize = 14)
ax.set_title('Average Product Price Distribution',fontsize = 14)

 
#%%





