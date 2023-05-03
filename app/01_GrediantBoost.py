import os
from utils.dataset import DatasetStack
from utils.compute import regular_feature, RegressionModel

from pyspark.ml.regression import DecisionTreeRegressor
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.regression import GBTRegressor
from pyspark.ml.regression import LinearRegression
from pyspark.ml.regression import GeneralizedLinearRegression
from pyspark.ml.tuning import ParamGridBuilder

Trainset_Path = '../datasets/app-dataset/full/train.csv'
Testset_Path = '../datasets/app-dataset/full/test.csv'
Airport_Info_Path = '../datasets/AIRPORTS_INFO.csv'
Save_Path = '../models/'
Log_Path = '../models/log-2023-04-30-GrediantBoost.log'


datasets = DatasetStack(airport_info_path=Airport_Info_Path)
datasets.load(Trainset_Path, 'train')
datasets.load(Testset_Path, 'test')

trainset = regular_feature(datasets['train'].dataframe(), True)
testset = regular_feature(datasets['test'].dataframe(), True)

log = {}

model_name = 'GrediantBoost'
model = RegressionModel(GBTRegressor, trainset, testset)
lr = model.model
grid = ParamGridBuilder().addGrid(lr.maxDepth, [5,6,7,8]).build()
kfolds_rmse = model.kfolds(grid, k=3)
train_rmse, train_r2 = model.train()
test_rmse, test_r2 = model.test()
log[model_name] = {
    'kfolds': {
        'params': grid,
        'rmse': kfolds_rmse,
        'best_param': model.best_param,
    },
    'train': {
        'rmse': train_rmse,
        'r2': train_r2
    },
    'test': {
        'rmse': test_rmse,
        'r2': test_r2
    }
}
print(model_name, log[model_name])


with open(Log_Path, 'w') as f:
    f.write(str(log))
