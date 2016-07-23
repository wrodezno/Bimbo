    # -*- coding: utf-8 -*-
"""
    Created on Wed Jul  6 15:24:17 2016
    
    @author: wrodezno
    Purpose: parse product table
"""

class GetData():

       
    def getProductData(self):   
        #Import libraries
        import numpy as np
        import pandas as pd 
        #%%
        #Load data
        productTableCSVDataLoc = "/home/wrodezno/Documents/Bimbo/Data/producto_tabla.csv"
        productData = pd.read_csv(productTableCSVDataLoc)
        #%%
        #Bran\d Names Checked off
        #NES  = ?
        #BIM = Bimbo 
        #BAR = BARCEL
        #WON = wonder bread
        #COR = Coronado
        #ORO = George Weston Limited – owner of the Oroweat brand 
        #LC = LC CORONA
        #TR = Tia Rosa
        #RIC = RICOLINO
        #LA = LonchiBon  maybe?
        #THO = THOMAS English Muffins 
        #LAR= Lara
        #AM = Panettone
        #AV = Not sure it seems that this product is owned my snapple
        #BRE= could be mistake ?
        #BRL = Could be a mistake?
        #CAR = ?
        #CC = Coca Cola
        
        #CHK = ?
        #VR = ?
        #VER = VERO?
        #TRI = ?
        #SUN  = ?
        #SUA = SUANDY
        #SL = To resurants
        #MLA = Marinela
        #MR =  Milpa Real
        #SKD = star gum 
        #SAN = Sanissimo
        #PUL = ?
        #NEC = ?
        #NAI = ?
        #MTB = ?
        #Msk = MASK Fresko
        #MR = Milpa Real 
        #MP = ?
        #MCM = ?
        #LON = Lonchibon
        #KOD = Kodyz
        #GV = ?
        #GBI= Galletas Gabi
        #EMB = ?
        #Diff = ?
        #DH = Del Hogar
        #%%
        #Get Brand Names
        brandNames = pd.Series([productData.NombreProducto[i].split(" ")[-2] for i in range(0,productData.shape[0])])
        
        #Kick out IDENTIFICADO and  1kg from the brandNames array.  Replace with NaN 
        falseBrandLog = (brandNames=='IDENTIFICADO') | (brandNames == '1kg')
        brandNames[falseBrandLog] = np.nan
        productData['Brands'] = brandNames
        
        
        #%%
        #Obtaining the weight of the product 
        numPieces = productData['NombreProducto'].str.extract('(\d+p\s)',expand = False).copy()
        numPieces = numPieces.str.replace("(P|p)"," ")
        productData['numPieces'] = numPieces
        
        #%%
        #%Weight of the product 
        prodWeightRaw = productData['NombreProducto'].str.lower().str.extract('(\d+g|\d+ml|\d+kg)',expand = False).copy()
        prodWeightNumeric = pd.to_numeric(prodWeightRaw.str.replace('g|kg|ml',""))
        
        
        #Note everything measured in Millimeters is a drink.  Impossible to convert to g
        #Only 48 products have ml measurements 
        #test = prodWeightRaw.str.contains('ml')
        #Only 56 percent of products have the number of pieces
        #test[test.isnull()] =False
        #productData.NombreProducto[test]
        
        #Transforms all Kg to g
        dummyFlag = prodWeightRaw.str.contains('kg')
        dummyFlag[dummyFlag.isnull()] =False
        prodWeightNumeric[dummyFlag] = 100*prodWeightNumeric
        
        #Adding to product table
        productData['prodWeightRaw'] = prodWeightRaw
        productData['prodWeightNumeric'] = prodWeightNumeric
        
        #%%
        #This could be product type or packaging types 
        questionNames = pd.Series(['McD','BK','Sp','TIR','NTE','MTA','Conv','Ch','TNB','MTB','CU','Prom', \
        'TAB','Tira','Cj','Cn','TN','Tn','Tir','ME','CU2','CA','Var','TBE','CC','CJM','CUB','TR',\
        'DIF','Dpy','AV','mas','CR2','MQ','CR1','MP','Temp','CE','CB2','CJ','Cin','KC'])
        

        productData['questionName'] =  pd.Series(np.repeat('',productData.shape[0]))
        counter= 0
        for col in questionNames:
            print 100*counter/float(len(questionNames))    
            tempFlag = productData.NombreProducto.str.lower().str.contains('\s' + col.lower() + '\s').copy()    
            tempStr = pd.Series(np.repeat(col,np.sum(tempFlag)))
            productData.loc[tempFlag,('questionName')] = productData['questionName'][tempFlag].str.cat(tempStr, sep = '_')
            counter+=1
            
        emptyStrFlag = productData['questionName'] == '' 
        productData.loc[emptyStrFlag,('questionName')] = np.nan
        return productData
                 
    '''     
    counter= 0
    for col in questionNames:
    print 100*counter/float(len(questionNames))    
    tempFlag = productData.NombreProducto.str.lower().str.contains('\s' + col.lower() + '\s').copy()
    productData[col] = tempFlag
       counter+=1
    '''         
    #%% 
    def getClientData(self):
        #The purpose of this script is to download the client data 
        import pandas as pd 
        #%%
        #Load data
        clientTableDataLoc =  "/home/wrodezno/Documents/Bimbo/Data/cliente_tabla.csv"
        clientData = pd.read_csv(clientTableDataLoc)
        clientData = clientData.drop_duplicates(subset = "Cliente_ID",keep = "first")
        return clientData
       
        
        
    #%%
    def getLocData(self):
        #The purpose of this script is to download the location data
        import pandas as pd 
        #%%
        #Load data
        locationTableLoc = "/home/wrodezno/Documents/Bimbo/Data/town_state.csv"
        locData = pd.read_csv(locationTableLoc)
        return locData
       
       
       #%%    
    def getDemandData(self,testCase,sample,fileName,weeks,myLimit,cust,custName):
        #input: testcase:Boolean variable.
        #               If the data we want is just to test code then code 1 else 0    
        #        weeks: List with str element numbers.
        #               List of weeks we want data from.
        #      myLimit: string.
        #               Number of random obs obtained in each weeks
        #      sample:  Boolean variable.
        #               If we need a ramdom sample of the data then 1, else 0
        #        cust:  Boolean
        #               If I want to return a file already saved
        #    custName:  pickle file name
        #Return: Demand data
        
        import pandas as pd
        import MySQLdb
        #import time
         
         
        if cust:
            demandData = pd.read_pickle(custName)
            return demandData
                 
         
        if testCase:
            demandDataLoc = "/home/wrodezno/Documents/Bimbo/Data/pyCodeTestCase.pkl"
            demandData = pd.read_pickle(demandDataLoc)
            return demandData
            
        else:
            
            
            #fileName = 'sampleTrainData_' + 'weeks_' + '_'.join(weeks) + '_' + time.strftime("%m_%d_%Y_%H_%M_%S") + '.pkl'
            
            if not sample:
    
                db=MySQLdb.connect(passwd="M4382vwr",user = "root",db="Bimbo")
                query = 'select * from train'
                dataAll = pd.read_sql(query,db)
                db.close() 
                dataAll.to_pickle(fileName)
                return dataAll
                
            else:
                        
                for i in xrange(len(weeks)):
                    print 'Currently in week ' + weeks[i]
                    query = 'select * from train where Semana = ' + weeks[i] + \
                    ' order by RAND()' +\
                    ' LIMIT ' + myLimit
            
                    db=MySQLdb.connect(passwd="M4382vwr",user = "root",db="Bimbo")
                        
                    if i ==0:
                        try:
                            dataAll = pd.read_sql(query,db)
                            db.close()  
                        except Exception as e:
                            del dataAll
                            db.close()    
                            print e
                            break
                    else:    
                
                        try:   
                            data = pd.read_sql(query,db)
                            frames = [dataAll, data]
                            dataAll = pd.concat(frames)
                            db.close()             
                        except Exception as e:
                            db.close()  
                            del dataAll               
                            print e
                            break
                        
                dataAll.to_pickle(fileName)     
                return dataAll   
                     
           
            
    #flag= productData.loc[:,('questionName')].isnull()
            
    #productData.loc[flag,'NombreProducto']
    


        
        
        
        
        
