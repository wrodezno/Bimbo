require(xgboost)
require(methods)
require(data.table)
require(magrittr)
require(mlr)
require(gridExtra)



#paramaters for xgboost 
param <- list("objective" = "reg:linear",
              "eval_metric" = "rmse")
nround = 50
relativeImportancePlotFileNames = "/home/wrodezno/Documents/Bimbo/Data/RPlotTest.pdf"





#Reading Data----
train <- fread('/home/wrodezno/Documents/Bimbo/Data/trainR.csv', header = T, stringsAsFactors = F)






#Parsing Data for R----
#Storing dependent variable
y <- train$Demanda_uni_equil
#Delete Customer ID
train[,Cliente_ID := NULL]
train[,Demanda_uni_equil := NULL]
#Remove the predictor from training data
train[, yName:=NULL, with = F]
#Turn trainData to a matrix to read into xgb-
trainMatrix <- train[,lapply(.SD,as.numeric)] %>% as.matrix



#Running XG Boost----
bst = xgboost(param=param, data = trainMatrix, label = y, nrounds=nround)




#Plot Relative Importance ----
# Get the feature real names
predNames <- dimnames(trainMatrix)[[2]]
# Compute feature importance matrix
importance_matrix <- xgb.importance(predNames, model = bst)
# Nice graph
implt <- xgb.plot.importance(importance_matrix[1:10,]) + theme_bw() 
ggsave(relativeImportancePlotFileNames,implt)








