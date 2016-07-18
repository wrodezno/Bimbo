# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 15:32:41 2016

@author: wrodezno
"""




import pandas as pd
import MySQLdb
import time
weeks  = ['3','4','5','6']
myLimit = str(200000)

fileName = 'sampleTrainData_' + 'weeks_' + '_'.join(weeks) + '_' + time.strftime("%m_%d_%Y_%H_%M_%S") + '.pkl'

saveLocation = '/home/wrodezno/Documents/Bimbo/Data/' + fileName

for i in xrange(len(weeks)):
    print 'Currently in week ' + weeks[i]

    query = 'select * from train where Semana = ' + weeks[2] + \
    ' order by RAND()' +\
    ' LIMIT ' + myLimit

    db=MySQLdb.connect(passwd="M4382vwr",user = "root",db="Bimbo")
        
    if i ==0:
        
        try:
            dataAll = pd.read_sql(query,db)
            db.close()  
        except Exception as e:
            db.close()                 
            print e
    
    else:    

        try:   
            data = pd.read_sql(query,db)
            db.close()             
        except Exception as e:
            db.close()                 
            print e
        

    frames = [dataAll, data]
    dataAll = pd.concat(frames)

#%%
dataAll.to_pickle(saveLocation) 




















