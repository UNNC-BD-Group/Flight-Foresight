from pyspark.ml.tuning import CrossValidator
from pyspark.ml.evaluation import RegressionEvaluator

class RegressionModel:
    
    def __init__(self, model, train_set, test_set):
        self.model = model(featuresCol='features', labelCol='labels')
        self.evaluator = RegressionEvaluator(predictionCol='prediction', labelCol='labels', metricName='rmse')
        self.r2 = RegressionEvaluator(predictionCol='prediction', labelCol='labels', metricName='r2')
        self.train_set = train_set
        self.test_set = test_set
        self.best_param = {}
        
    def kfolds(self, grid, k=3):
        cv = CrossValidator(estimator=self.model, estimatorParamMaps=grid,
                            evaluator=self.evaluator, parallelism=1,
                            numFolds=k)
        cv = cv.fit(self.train_set)
        self.kfolds_performance = cv.avgMetrics
        index = cv.avgMetrics.index(min(cv.avgMetrics))
        self.best_param = grid[index]
        return cv.avgMetrics
    
    def train(self):
        self.model = self.model.fit(self.train_set, self.best_param)
        pred = self.model.transform(self.train_set)
        return (self.evaluator.evaluate(pred), self.r2.evaluate(pred))
    
    def test(self):
        pred = self.model.transform(self.test_set)
        return (self.evaluator.evaluate(pred), self.r2.evaluate(pred))
    
    def predict(self):
        return self.model.transform(self.test_set)
    
    def save(self, path='./model'):
        self.model.write.save(path)