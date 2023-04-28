import os
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
import pandas as pd
import uuid
from tqdm import tqdm
from datetime import datetime


class Dataset:
    
    def __init__(self, path='', spark_master='local', echo=True, spark_frame=None, spark_handle=None):
        self.echo = echo
        
        if spark_frame is None:
            if spark_handle is None:
                self._load_spark(spark_master)
            else:
                self._spark_handle = spark_handle
                self._spark_master = 'Sub'
                self._spark_app_name = 'Sub'
            self._load_data(path)
        else:
            self._spark_master = 'Sub'
            self._spark_app_name = 'Sub'
            self._spark_data_frame = spark_frame
            self.path = ''
            self._spark_handle = spark_handle
            
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
        
        if not os.path.isfile(path):
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
        
        else:
            self._spark_data_frame = self._spark_handle.read.option("header", True).option("inferSchema", True).csv(path)
            
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
    
    def save(self, path='./', encoding='utf-8'):
        self.dataframe('pandas').to_csv(path, sep=',', header=True, encoding=encoding)
    
class AirDelayDataset(Dataset):
    
    def __init__(self, path='', spark_master='local',
                 echo=True, spark_frame=None, spark_handle=None,
                 airport_data_path='./', carrier_data_path='./'):
        
        super().__init__(path, spark_master, echo, spark_frame, spark_handle)
        self.airport_data_path = airport_data_path
        self.carrier_data_path = carrier_data_path
    
    def get_date_period(self, start='2009-01-01', end='2009-01-02'):
        spark_frame = self._spark_data_frame.filter(
                self._spark_data_frame['FL_DATE'] >= start).filter(
                self._spark_data_frame['FL_DATE'] < end
            )
        return self.derive(spark_frame)
    
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
            
        spark_frame = self._spark_data_frame.filter(
                self._spark_data_frame[key] >= delay_time_range[0]).filter(
                    self._spark_data_frame[key] < delay_time_range[1]
            )
                                  
        return self.derive(spark_frame)
    
    def get_arrival_delay(self, delay_time_range=(0, 10)):
        return self.get_delay(delay_time_range, 'arrival')
    
    def get_arrival_delay(self, delay_time_range=(0, 10)):
        return self.get_delay(delay_time_range, 'departure')
    
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
        return self.derive(frame)
    
    def get_origin_ports(self, ports=[]):
        return self.get_ports(ports, 'origin')
    
    def get_dest_ports(self, ports=[]):
        return self.get_ports(ports, 'dest')
    
    def get_cancelled(self, code=None):
        '''
        code = None | 'A' | 'B' | 'C' | 'D'
        '''
        frame = self._spark_data_frame.filter(
                self._spark_data_frame['CANCELLED'] == 1
            )
        if code is not None:
            frame = frame.filter(self._spark_data_frame['CANCELLATION_CODE'] == code)
        return self.derive(frame)
        
    def get_distance(self, distance=(0, 500)):
        spark_frame = self._spark_data_frame.filter(
                self._spark_data_frame['DISTANCE'] >= distance[0]).filter(
                    self._spark_data_frame['DISTANCE'] < distance[1]
            )
        return self.derive(spark_frame)
        
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
        
        spark_frame = self._spark_data_frame.filter(
            self._spark_data_frame[item] >= period[0]).filter(
                self._spark_data_frame[item] < period[1]
            )  
        return self.derive(spark_frame)
    
    def get_departure_time(self, period=(0000, 2400)):
        return self.get_time_period(period, 'departure')
    
    def get_arrival_time(self, period=(0000, 2400)):
        return self.get_time_period(period, 'arrival')
    
    def get_wheels_on_time(self, period=(0000, 2400)):
        return self.get_time_period(period, 'wheels_on')
    
    def get_wheels_off_time(self, period=(0000, 2400)):
        return self.get_time_period(period, 'wheels_off')
    
    def get_taxi_out_time(self, period=(0000, 2400)):
        return self.get_time_period(period, 'taxi_out')
    
    def get_taxi_in_time(self, period=(0000, 2400)):
        return self.get_time_period(period, 'taxi_in')
    
    def attach_airport_info(self, mode='both'):
        frame = self._spark_handle.read.option("header", True).option("inferSchema", True).csv(self.airport_data_path)
        if mode == 'origin':
            frame = frame.select(['iata_code', 'latitude_deg', 'longitude_deg', 'iso_region'])
            frame = frame.withColumnRenamed('iata_code', 'ORIGIN')
            frame = frame.withColumnRenamed('latitude_deg', 'ORIGIN_LAT')
            frame = frame.withColumnRenamed('longitude_deg', 'ORIGIN_LON')
            frame = frame.withColumnRenamed('iso_region', 'ORIGIN_REGION')
            data = self.dataframe(type='spark').join(frame, on='ORIGIN', how='left_outer')
        elif mode == 'both':
            frame = frame.select(['iata_code', 'latitude_deg', 'longitude_deg', 'iso_region'])
            frame = frame.withColumnRenamed('iata_code', 'ORIGIN')
            frame = frame.withColumnRenamed('latitude_deg', 'ORIGIN_LAT')
            frame = frame.withColumnRenamed('longitude_deg', 'ORIGIN_LON')
            frame = frame.withColumnRenamed('iso_region', 'ORIGIN_REGION')
            data = self.dataframe(type='spark').join(frame, on='ORIGIN', how='left_outer')
            frame = frame.withColumnRenamed('ORIGIN', 'DEST')
            frame = frame.withColumnRenamed('ORIGIN_LAT', 'DEST_LAT')
            frame = frame.withColumnRenamed('ORIGIN_LON', 'DEST_LON')
            frame = frame.withColumnRenamed('ORIGIN_REGION', 'DEST_REGION')
            data = data.join(frame, on='DEST', how='left_outer')
        elif mode == 'dest':
            frame = frame.withColumnRenamed('iata_code', 'DEST')
            frame = frame.withColumnRenamed('latitude_deg', 'DEST_LAT')
            frame = frame.withColumnRenamed('longitude_deg', 'DEST_LON')
            frame = frame.withColumnRenamed('iso_region', 'DEST_REGION')
            data = self.dataframe(type='spark').join(frame, on='DEST', how='left_outer')
        else:
            return None
        return self.derive(data)
    
    def derive(self, spark_dataframe):
        return AirDelayDataset(
            spark_frame = spark_dataframe,
            airport_data_path = self.airport_data_path,
            carrier_data_path = self.carrier_data_path,
            spark_handle = self._spark_handle
        )
    
    def random_sample(self, fraction=0.1, seed=0):
        return self.derive(self._spark_data_frame.sample(fraction, seed))
    
    def count_airport(self, port='origin'):
        if port == 'origin':
            key = 'ORIGIN'
        elif key == 'dest':
            key = ' DEST'
        else:
            key = 'ORIGIN'
        return self._spark_data_frame.groupBy(key).count().orderBy('count', ascending=False).toPandas()
    
    def count_airline(self):
        return self._spark_data_frame.groupBy(['ORIGIN', 'DEST']).count().orderBy('count', ascending=False).toPandas()