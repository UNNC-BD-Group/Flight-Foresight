from pyspark.ml.feature import StandardScaler, VectorAssembler, StringIndexer
from pyspark.ml import Pipeline
from pyspark.sql.functions import month, dayofmonth

def regular_feature(dataframe, standard = False, fill=0):
    
    dataframe = dataframe.fillna(fill)
    date = dataframe.select('FL_DATE',
                 month(dataframe['FL_DATE']).alias('FL_DATE_MONTH'),
                 dayofmonth(dataframe['FL_DATE']).alias('FL_DATE_DAY'))
    dataframe = dataframe.join(date, on='FL_DATE', how='left_outer')
    
    indexer = StringIndexer(inputCol='OP_CARRIER', outputCol='OP_CARRIER_INDEX')
    
    if standard:
        assembler = VectorAssembler(
        inputCols=[
                'FL_DATE_MONTH', 'FL_DATE_DAY', 'ORIGIN_LAT', 'ORIGIN_LON', 'DEST_LAT', 'DEST_LON',
                'DEP_TIME', 'DEP_DELAY', 'OP_CARRIER_INDEX', 
                'DISTANCE', 'CARRIER_DELAY', 'WEATHER_DELAY', 'NAS_DELAY',
                'SECURITY_DELAY', 'LATE_AIRCRAFT_DELAY'
            ],
            outputCol='features_'
        )
        standard = StandardScaler(inputCol='features_', outputCol='features')
        model_agg = Pipeline(stages = [indexer, assembler, standard])
        model_agg = model_agg.fit(dataframe)
        return model_agg.transform(dataframe).withColumnRenamed('ARR_DELAY', 'labels')
    
    else:
        assembler = VectorAssembler(
        inputCols=[
                'FL_DATE_MONTH', 'FL_DATE_DAY', 'ORIGIN_LAT', 'ORIGIN_LON', 'DEST_LAT', 'DEST_LON',
                'DEP_TIME', 'DEP_DELAY', 'OP_CARRIER_INDEX', 
                'DISTANCE', 'CARRIER_DELAY', 'WEATHER_DELAY', 'NAS_DELAY',
                'SECURITY_DELAY', 'LATE_AIRCRAFT_DELAY'
            ],
            outputCol='features'
        )
        model_agg = Pipeline(stages = [indexer, assembler])
        model_agg = model_agg.fit(dataframe)
        return model_agg.transform(dataframe).withColumnRenamed('ARR_DELAY', 'labels')
    