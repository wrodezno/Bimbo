"""
Spyder Editor

This is a temporary script file.
Purpose: To explore data through plotting.
         Will Only explore a subsample of data from the first two weeks
"""

#%%
def exploreData():
    #Importing libraries 
    import os
    os.chdir("/home/wrodezno/Documents/Bimbo/Code")
    import seaborn as sns
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd 
    from subFun.GetData import GetData
    from matplotlib.backends.backend_pdf import PdfPages
    #%%
    #Functions which will be used repeatedly throughout. 
    
    def hbars(colrow,colcol,groupedData,tempcolors,title,ylab,xlab):
        #Input: colrow: Values alone the x axis
        #       colcol: Values along the y-axis
        #  groupedData: Pandas DataFrame
        #   tempcolors: Bar colors in plot
        #        title: Plot title
        #        ylab:  Y-label
        #        xlab:  X-label
        #Output: Horizontal Bar Plot with value labels the the end of each bar
        valuePlotting = sns.barplot(x = colcol,y = colrow,order = groupedData[colcol],data = groupedData)
        fig, ax = plt.subplots()                                                       #Plot Figure and axes handles 
        fig.set_size_inches(14, 14)
        sns.despine()
        ax = sns.barplot(x = colrow,y = colcol,data = groupedData,order = groupedData[colcol], color = tempcolors)
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
        return fig
            
            
    
    
    
    
    
    def perc_hist(x, **kwargs):
        #Input: x: Pandas Series
        #Output: Histogram with y axis showing the percentage of values in a
        #        given bin.
        myBins = np.arange(0,40,2)
        myBins = np.append(myBins,np.inf)    
        categories = [ '(' + str(myBins[i]) + ',' +   str(myBins[i+1])      +    ']' for i in  range(len(myBins)-1)      ]    
        binCategories = pd.cut(x,bins = myBins,labels = categories)
        myCount = []    
        for b in categories:
            tempCount = np.sum(binCategories.isin([b]))
            myCount.append(tempCount)
        myCount = np.array(myCount)    
        myPerc =  100*myCount/np.sum(myCount)       
        categories = np.array(categories)   
        sns.set_style('whitegrid')
        ax = sns.barplot(x = categories,y = myPerc,**kwargs)
        ax.set_xticklabels(categories,rotation='vertical')
    
    
    
    myColors = {'orange': [255/float(255),127/float(255),14/float(255)],\
    'blue':[95/float(255),158/float(255),209/float(255)],\
    'red': [214/float(255),39/float(255),40/float(255)],\
    'green':[103/float(255),191/float(255),92/float(255)],\
    'brown':[168/float(255),120/float(255),110/float(255)],\
    'darkGreen':[44/float(255),160/float(255),44/float(255)]}
    
    
    #%%
    #Loading data
    
    getData = GetData()
    clientData = getData.getClientData()
#    locData = getData.getLocData()
    productData = getData.getProductData()
    demandData = getData.getDemandData(testCase = True,sample = False,fileName = '',weeks = '',myLimit = '',cust = False,custName = '')
#    demandData = demandData.loc[:70000,:]
    
    #%%
    #Creating Data Tables which will be used for plotting 
    
        
        
        
    #Adding price to the demand data
    pricePerUnit = demandData.Venta_hoy/demandData.Venta_uni_hoy
    demandData['pricePerUnit'] = pricePerUnit
    demandData['pricePerUnitLogged'] = np.log10(pricePerUnit)
    demandData['DemandLogged'] = np.log10(demandData.Demanda_uni_equil)
    
        
        
        
    
    #Brand Demand Table 
    productDemandLinkData = pd.merge(demandData, productData, how='left', on=['Producto_ID'],sort=False)
    brandGroupedData = productDemandLinkData.groupby('Brands')
    brandGroupedData = brandGroupedData['Demanda_uni_equil'].agg([np.mean, np.std,np.sum,np.median]).sort_values('median',ascending = True)
    brandGroupedData['Brands'] = brandGroupedData.index
    
    
    
    
    
    #Canal Demand Data
    groupedCanalData = demandData.groupby('Canal_ID')
    groupedCanalData = groupedCanalData['Demanda_uni_equil'].agg([np.mean, np.std,np.sum,np.median]).sort_values('median',ascending = True)
    groupedCanalData['Canal_ID'] = groupedCanalData.index
    groupedCanalData['Canal_ID'] =  groupedCanalData['Canal_ID'].astype('category')
    
    
    
    
    
    #Product Price Data
    productPriceTable = demandData.loc[:,('Producto_ID','pricePerUnit')]
    productPriceGroupedData = productPriceTable.groupby('Producto_ID')
    productPriceGroupedData = productPriceGroupedData['pricePerUnit'].agg([np.mean, np.std])
    productPriceGroupedData['cv'] = 100*productPriceGroupedData['std']/productPriceGroupedData['mean']
    productPriceGroupedData = productPriceGroupedData.loc[~productPriceGroupedData['cv'].isnull()]
    
    
    
    #%%
    #Creating Exploratory Plots
    
    with PdfPages('multipage_pdf.pdf') as pdf:
    
        #Customer ID Investigation 
    
        #Histogram of customer ids        
        sns.set_style("whitegrid")
        f, ax = plt.subplots(figsize=(20, 10))
        maxBound = 10000000
        jumps = 500000
        myBounds = range(0,maxBound,jumps)
        myBounds.append(np.inf)
        myXTicks = range(0,maxBound+jumps,jumps)
        ax = sns.distplot(clientData.Cliente_ID,kde = False,rug = False,hist = True,bins = myBounds,ax=ax,color = myColors['blue'])    
        ax.set_xticks(myXTicks)
        ax.set_xlim((0,maxBound))
        xx = ax.get_xticks()
        ll = ['%.0f' % a for a in xx]
        ax.set_xticklabels(ll)
        ax.set_ylabel('Count',fontsize = 12)
        ax.set_xlabel('Customer ID',fontsize = 14)
        ax.set_title('Customer Id Histogram',fontsize = 16)
        f.savefig(pdf, format='pdf')
         
    #%
        #Grouping the Client Ids and ploting distribution within groups. Box Plot
        myBins = np.array([0,2500000,4000000,5000000,7000000,8500000,np.inf])
        binCategories = pd.cut(clientData.Cliente_ID,bins = myBins)
        clientData['customerBins'] = binCategories
        custDemMergekData = pd.merge(demandData, clientData, how='left', on=['Cliente_ID'],sort=False)
        fig, ax = plt.subplots()                                                       
        fig.set_size_inches(11, 10)
        ax = sns.boxplot(y = 'Demanda_uni_equil',x = 'customerBins' ,vert=1,data = custDemMergekData,color = myColors['orange'])
        ax.set_title('Mystery Variable Distribution',fontsize = 16)
        ax.set_ylabel('Customer ID Bins',fontsize = 14)
        ax.set_xlabel('Demand',fontsize=14)
        fig.savefig(pdf, format='pdf')
    
    #%
        #Grouping the Client Ids and ploting distribution within groups. Box Plot Closer Look
        myBins = np.array([0,2500000,4000000,5000000,7000000,8500000,np.inf])
        binCategories = pd.cut(clientData.Cliente_ID,bins = myBins)
        clientData['customerBins'] = binCategories
        custDemMergekData = pd.merge(demandData, clientData, how='left', on=['Cliente_ID'],sort=False)
        fig, ax = plt.subplots()                                                       
        fig.set_size_inches(11, 10)
        ax = sns.boxplot(y = 'Demanda_uni_equil',x = 'customerBins' ,vert=1,data = custDemMergekData,color = myColors['orange'])
        ax.set_title('Mystery Variable Distribution',fontsize = 16)
        ax.set_ylabel('Customer ID Bins',fontsize = 14)
        ax.set_xlabel('Demand',fontsize=14)
        #ax.set_ylim(brandGroupedData(0,20))
        fig.savefig(pdf, format='pdf')
    
    
    #%
        #Grouping the Client Ids and ploting distribution within groups. Histogram
        g = sns.FacetGrid(custDemMergekData, col="customerBins", size=10,aspect=.78)
        g.map(perc_hist, "Demanda_uni_equil",color = myColors['orange']);
        g.set(xlabel = 'Demand',ylabel = 'Percentage')
        g.savefig(pdf, format='pdf')
        
        
        
        
        
    
    #%
    #Product Brand vs Demand
        
    #%
    #Boxplot Brand vs Demand 
        fig, ax = plt.subplots()                                                       #Plot Figure and axes handles 
        fig.set_size_inches(14, 8.27) 
        sns.set_style("whitegrid")
        ax = sns.boxplot(x="Demanda_uni_equil", y="Brands", data=productDemandLinkData,order = brandGroupedData['Brands'],color = myColors['red'])
        #ax.set_xticklabels(ax.get_xticklabels(),rotation='vertical')
        ax.set_ylabel('Brands',fontsize = 15)
        ax.set_xlabel('Demand',fontsize = 15)
        ax.set_title('Brand Demand Distribution',fontsize = 14)
        fig.savefig(pdf, format='pdf')    
    
    #%
        #Box Plot Closer look Brand vs Demand 
        fig, ax = plt.subplots()                                                       #Plot Figure and axes handles 
        fig.set_size_inches(14, 8.27) 
        sns.set_style("whitegrid")
        ax = sns.boxplot(x="Demanda_uni_equil", y="Brands", data=productDemandLinkData,order = brandGroupedData['Brands'],color = myColors['red'])
        #ax.set_xticklabels(ax.get_xticklabels(),rotation='vertical')
        ax.set_ylabel('Brands',fontsize = 15)
        ax.set_xlabel('Demand',fontsize = 15)
        ax.set_title('Brand Demand Distribution',fontsize = 14)
        ax.set_xlim((0,75.5))
        fig.savefig(pdf, format='pdf') 
    
    #%
        #Plotting Median Demand per Brand 
        fig = hbars('median','Brands',brandGroupedData,myColors['red'],'Median Demand per Brand','Brands','Median Demand')
        fig.savefig(pdf, format='pdf') 
    
    
    

    #%
    #Canal ID

    
    #%
        #Box Plot Canal vs Demand
    
        fig, ax = plt.subplots()                                                       #Plot Figure and axes handles 
        fig.set_size_inches(14, 8.27) 
        sns.set_style("whitegrid")
        ax = sns.boxplot(x="Canal_ID", y="Demanda_uni_equil", data=demandData, order = groupedCanalData.index,color = myColors['brown'])
        fig.savefig(pdf, format='pdf')
    #%
        #Box Plot Canal vs Demand. Closer Look
        fig, ax = plt.subplots()                                                       #Plot Figure and axes handles 
        fig.set_size_inches(14, 8.27) 
        sns.set_style("whitegrid")
        ax = sns.boxplot(x="Canal_ID", y="Demanda_uni_equil", data=demandData, order = groupedCanalData.index,color = myColors['brown'])
        ax.set_ylim((0,75.5))
        fig.savefig(pdf, format='pdf')
    #%
    
        #Median per groupdemandData = demandData.loc[:70000,:]
    
        fig = hbars('median','Canal_ID',groupedCanalData,myColors['brown'],'Median Demand per Canal','Canal_ID','Median Demand')
        fig.savelocData.groupby(['Town','State']).count()
        fig(pdf, format='pdf')
        
        
        
        
    #%
    #Does Price have an effect on Demand?
    
        #Price vs Demand Scatter Plot
        fig, ax = plt.subplots()                                                       #Plot Figure and axes handles 
        fig.set_size_inches(14, 8.27) 
        sns.set_style("whitegrid")
        ax = sns.regplot(x="pricePerUnit", y="Demanda_uni_equil", data=demandData,scatter_kws=dict(alpha=.5),fit_reg = False,color = myColors['darkGreen'])   
        ax.set_xlabel('Price Per Unit',fontsize = 14)
        ax.set_ylabel('Number of Units Demanded',fontsize = 14)
        ax.set_title('Unit Price vs Demand',fontsize = 16)
        ax.set_ylim((0,np.max(demandData['Demanda_uni_equil'])))
        #ax.set_xlim((0,np.max(demandData['pricePerUnit'])))
        ax.set_xlim((0,50))
        fig.savefig(pdf, format='pdf')
    
    
    
    #%
        #Prices Logged vs Demand Logged scatter plot
        fig, ax = plt.subplots()                                                       #Plot Figure and axes handles 
        fig.set_size_inches(14, 8.27) 
        sns.set_style("whitegrid")
        ax = sns.regplot(x="pricePerUnitLogged", y="DemandLogged", data=demandData,scatter_kws=dict(alpha=.5),color = myColors['darkGreen'])  
        #ax.set_xlim((0,200))
        #ax.set_ylim((0,40))
        ax.set_xlabel('Price Per Unit Logged',fontsize = 14)
        ax.set_ylabel('Number of Units Demanded',fontsize = 14)
        ax.set_title('Unit Price Logged vs Demand',fontsize = 16)
        ax.set_ylim((0,np.max(demandData['DemandLogged'])))
        ax.set_xlim((0,np.max(demandData['pricePerUnitLogged'])))
        fig.savefig(pdf, format='pdf')
    
    
        #How much do prices vary within a product.  Average price variation within produect 
    #%
        f, ax = plt.subplots()                                                     #Plot Figure and axes handles 
        fig.set_size_inches(14, 8.27) 
        sns.set_style("whitegrid")
        ax = sns.distplot(productPriceGroupedData['cv'],rug=True,color = myColors['darkGreen'])
        ax.set_xlabel('Coefficient of Variation',fontsize = 14)
        ax.set_ylabel('Count',fontsize = 14)
        ax.set_title('Price Coefficient of Variation per Product',fontsize = 14)
        f.savefig(pdf, format='pdf')
    #%
        #Mean Price Distribution 
        f, ax = plt.subplots()                                                     #Plot Figure and axes handles 
        fig.set_size_inches(14, 8.27) 
        ax = sns.distplot(productPriceGroupedData['mean'],rug=True,color = myColors['darkGreen'])
        ax.set_xlabel('Mean Price',fontsize = 14)
        ax.set_ylabel('Count',fontsize = 14)
        ax.set_title('Average Product Price Distribution',fontsize = 14)
        f.savefig(pdf, format='pdf')
     
    
    
     
     
     #%%
    #Geo Data
    
    
    
    

 
     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    '''
    
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
        
    
        #%
        #Box Plot Mystery variable vs Demand
        fig, ax = plt.subplots()                                                       
        fig.set_size_inches(14, 13.27)
        ax = sns.boxplot(data=boxes,orient = 'h',color = myColors['green'])
        ax.set_title('Mystery Variable Distribution',fontsize = 18)
        ax.set_ylabel('Variable',fontsize = 16)
        ax.set_xlabel('Demand',fontsize=16)
        #ax.set_xlim((-0.1,48.5))
        ax.set_yticklabels(ylabels)
        fig.savefig(pdf, format='pdf') 
        
        #Box Plot Mystery variable vs Demand. Closer Look
        fig, ax = plt.subplots()                                                       
        fig.set_size_inches(14, 13.27)
    
    
        ax = sns.boxplot(data=boxes,orient = 'h',color = myColors['green'])
        ax.set_title('Mystery Variable Distribution',fontsize = 18)
        ax.set_ylabel('Variable',fontsize = 16)
        ax.set_xlabel('Demand',fontsize=16)
        ax.set_xlim((0,75.5))
        ax.set_yticklabels(ylabels)
        fig.savefig(pdf, format='pdf') 
   
   
    #%
    #Culmative Demand per mystery variable 
        valuePlotting = sns.barplot(x = ylabels,y = demanvarPlot)
        fig, ax = plt.subplots()                                                       #Plot Figure and axes handles 
        fig.set_size_inches(14, 14)
        sns.despine()
        sns.set_style("whitegrid")
        ax = sns.barplot(x = demanvarPlot,y = ylabels,color = myColors['green'])
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
        fig.savefig(pdf, format='pdf')
        
'''  
    
    
    '''
    #Do any two states have the same town? 
     t = locData.State[0]
    towns = locData.Town
    cityCount = []
    for town in towns:
        tempFlag = locData.Town.isin([town])
        tempCityCount = len(locData.State[tempFlag].unique())
        cityCount.append(tempCityCount)
    cityCountArray = np.array(cityCount)    
    moreThanOneStateFlag =   cityCountArray > 1
    townOfInterest = towns[moreThanOneStateFlag] 
    locData.loc[locData.Town.isin(townOfInterest),:]
    '''
    
    
    
    
    
