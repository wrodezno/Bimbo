# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 15:32:41 2016

@author: wrodezno
"""



def getDemandData(testCase,sample,fileName,weeks,myLimit):
    #input: testcase:Boolean variable.
    #               If the data we want is just to test code then code 1 else 0    
    #        weeks: List with str element numbers.
    #               List of weeks we want data from.
    #      myLimit: string.
    #               Number of random obs obtained in each weeks
    #      sample:  Boolean variable.
    #               If we need a ramdom sample of the data then 1, else 0    
    
    import pandas as pd
    import MySQLdb
    #import time
     
    if testCase:
        demandDataLoc = "/home/wrodezno/Documents/Bimbo/Data/pyCodeTestCase.csv"
        demandCol =['Semana','Agencia_ID','Canal_ID','Ruta_SAK','Cliente_ID','Producto_ID','Venta_uni_hoy',\
        'Venta_hoy','Dev_uni_proxima','Dev_proxima','Demanda_uni_equil']
        demandData = pd.read_csv(demandDataLoc,names = demandCol)
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
            #%%

        
        
        
        
        
        
        
        
        
    
    






