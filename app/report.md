## Comparison
|Model|Train RMSE|Train $R^2$|Test RMSE|Test $R^2$|
|:--|:---|:---|:---|:---|
|DecisionTree|17.9888|0.7935|30.2331|0.6314|
|GrediantBoost|18.9884|0.7700|27.4730|0.6956|
|GuassionRegression|9.4382|0.9432|14.5720|0.9144|
|LinearRegression|9.4382|0.9432|14.5720|0.9144|
|RandomForest|17.4475|0.8058|29.1984|0.6562|
## Models
### DecisionTree
#### K-Folds
|Parameter|RMSE|
|:-----:|:---|
|`maxDepth=5`|19.9180|
|`maxDepth=6`|19.2813|
|`maxDepth=7`|18.4950|
|**`maxDepth=8`**|**17.8724**|
#### Performance
|Fold|RMSE|$R^2$|
|:---:|:---|:---|
|Train|17.9888|0.7935|
|Test|30.2331|0.6314|
### GrediantBoost
#### K-Folds
|Parameter|RMSE|
|:-----:|:---|
|`maxDepth=2`, `maxIter=5`, `maxMemoryInMB=64`|21.8440|
|`maxDepth=3`, `maxIter=5`, `maxMemoryInMB=64`|20.9204|
|`maxDepth=4`, `maxIter=5`, `maxMemoryInMB=64`|19.7064|
|**`maxDepth=5`, `maxIter=5`, `maxMemoryInMB=64`**|**18.9748**|
#### Performance
|Fold|RMSE|$R^2$|
|:---:|:---|:---|
|Train|18.9884|0.7700|
|Test|27.4730|0.6956|
### GuassionRegression
#### K-Folds
|Parameter|RMSE|
|:-----:|:---|
|**`family=gaussian`, `tol=0.0001`**|**9.4384**|
|`family=gaussian`, `tol=1e-05`|9.4384|
|`family=gaussian`, `tol=1e-06`|9.4384|
|`family=gaussian`, `tol=1e-07`|9.4384|
#### Performance
|Fold|RMSE|$R^2$|
|:---:|:---|:---|
|Train|9.4382|0.9432|
|Test|14.5720|0.9144|
### LinearRegression
#### K-Folds
|Parameter|RMSE|
|:-----:|:---|
|**`tol=10000.0`**|**9.4384**|
|`tol=1000.0`|9.4384|
|`tol=100.0`|9.4384|
|`tol=10.0`|9.4384|
|`tol=1.0`|9.4384|
#### Performance
|Fold|RMSE|$R^2$|
|:---:|:---|:---|
|Train|9.4382|0.9432|
|Test|14.5720|0.9144|
### RandomForest
#### K-Folds
|Parameter|RMSE|
|:-----:|:---|
|`maxDepth=5`|20.4030|
|`maxDepth=6`|19.4154|
|`maxDepth=7`|18.4195|
|**`maxDepth=8`**|**17.4223**|
#### Performance
|Fold|RMSE|$R^2$|
|:---:|:---|:---|
|Train|17.4475|0.8058|
|Test|29.1984|0.6562|
