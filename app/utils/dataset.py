import os
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
import pandas as pd
import uuid
from tqdm import tqdm
from datetime import datetime


class Dataset:
    
    def __init__(self, path='', spark_master='local', echo=True, spark_frame=None):
        self.echo = echo
        
        if spark_frame is None:
            self._load_spark(spark_master)
            self._load_data(path)
        else:
            self._spark_master = 'Sub'
            self._spark_app_name = 'Sub'
            self._spark_data_frame = spark_frame
            self.path = ''
            
            
    def _load_spark(self, master='local'):
        if self.echo:
            print('Initializing Spark...')
        self._spark_master = master
        self._spark_app_name = str(uuid.uuid4())
        conf = SparkConf().setMaster(master).setAppName(self._spark_app_name)
        sc = SparkContext(conf = conf)
        self._spark_handle = SparkSession(sc)
        if self.echo:
            print('Spark stand by (Master={}, AppName={})'.format(self._spark_master, self._spark_app_name))
        return self._spark_app_name
            
    def _load_data(self, path):
        self.path = path
        if self.echo:
            print('Load datasets from {}'.format(path))
        frames = []
        
        for root, _, files in os.walk(path):
            enumerator = enumerate(files)
            if self.echo:
                enumerator = tqdm(enumerator)
            for i, file in enumerator:
                if '.csv' in file:
                    if self.echo:
                        enumerator.set_description('Loading {}'.format(file))
                    frame = self._spark_handle.read.option("header", True).option("inferSchema", True).csv(os.path.join(root, file))
                    frames.append(frame)
        if self.echo:
            print('Merging Frames...')
        if len(frames) > 0:
            self._spark_data_frame = frames[0]
            for i in range(1, len(frames)):
                self._spark_data_frame = self._spark_data_frame.unionByName(frames[i], allowMissingColumns=True)
        else:
            self._spark_data_frame = self._spark_handle.createDataFrame([])
            
        if self.echo:
            print(self.status())
            
    def __len__(self):
        return self._spark_data_frame.count()
    
        
    def status(self):
        _status = pd.DataFrame(
            data=[self._spark_master,
                  self._spark_app_name,
                  self.path,
                  len(self)
                  ],
            index=[
                'Spark Master', 'Spark APP Name', 'Data Path', 'Data Count'
            ]
        )
        return _status
    
    def __repr__(self):
        return repr(self.status())
    
    def __str__(self):
        return str(self.status)
    
    def dataframe(self, type='spark'):
        '''
        type = 'spark' | 'pandas' 
        '''
        if type == 'spark':
            return self._spark_data_frame
        elif type == 'pandas':
            return self._spark_data_frame.toPandas()
        return None
    
class AirDelayDataset(Dataset):
    
    def get_date_period(self, start='2009-01-01', end='2009-01-02'):
        return AirDelayDataset(
            spark_frame = self._spark_data_frame.filter(
            self._spark_data_frame['FL_DATE'] >= start).filter(
                self._spark_data_frame['FL_DATE'] < end
            )
            )
    
    def get_delay(self, delay_time_range=(0, 10), type='arrival'):
        '''
        type = 'departure' | 'arrival'
        '''
        if type == 'departure':
            key = 'DEP_DELAY'
        elif type == 'arrival':
            key = 'ARR_DELAY'
        else:
            key = 'ARR_DELAY'
                                  
        return AirDelayDataset(
            spark_frame = self._spark_data_frame.filter(
            self._spark_data_frame[key] >= delay_time_range[0] & self._spark_data_frame[key] < delay_time_range[1]
        ))
        
    def get_ports(self, ports=[], type='origin'):
        '''
        type = 'origin' | 'dest'
        '''
        frame = None
        if type == 'origin':
            key = 'ORIGIN'
        elif type == 'dest':
            key = 'DEST'
        else:
            key = 'ORIGIN'
            
        for port in ports:
            frame_ = self._spark_data_frame.filter(
                self._spark_data_frame[key] == port
            )
            if frame is None:
                frame = frame_
            else:
                frame.unionByName(frame_, allowMissingColumns=True)
        return AirDelayDataset(spark_frame = frame)
    
    def get_cancelled(self, code=None):
        '''
        code = None | 'A' | 'B' | 'C' | 'D'
        '''
        frame = self._spark_data_frame.filter(
                self._spark_data_frame['CANCELLED'] == 1
            )
        if code is not None:
            frame = frame.filter(self._spark_data_frame['CANCELLATION_CODE'] == code)
        return AirDelayDataset(
            spark_frame = frame
        )
        
    def get_distance(self, distance=(0, 500)):
        
        return AirDelayDataset(
            spark_frame = self._spark_data_frame.filter(
            self._spark_data_frame['DISTANCE'] >= distance[0] & self._spark_data_frame['DISTANCE'] < distance[1]
        ))
        
    def get_time_period(self, period=(0000, 2400), item='departure'):
        '''
        item = 'crs_departure' | 'departure' | 'taxi_out' | 'taxi_in' | 
                'wheels_on' | 'wheels_off' | 'arrival' | 'crs_arrival'
        '''
        if item == 'departure':
            item = 'DEP_TIME'
        elif item == 'crs_departure':
            item = 'CRS_DEP_TIME'
        elif item == 'taxi_out':
            item = 'TAXI_OUT'
        elif item == 'taxi_in':
            item = 'TAXI_IN'
        elif item == 'wheels_on':
            item = 'WHEELS_ON'
        elif item == 'wheels_off':
            item = 'WHEELS_OFF'
        elif item == 'arrival':
            item = 'ARR_TIME'
        elif item == 'crs_arrival':
            item = 'CRS_ARR_TIME'
        else:
            item = 'DEP_TIME'
            
        return AirDelayDataset(
            spark_frame = self._spark_data_frame.filter(
            self._spark_data_frame[item] >= period[0] & self._spark_data_frame[item] < period[1]
        ))