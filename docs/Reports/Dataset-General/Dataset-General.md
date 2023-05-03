# Dataset Analysis

## Features
|Column|Table Token      |Type                |Description|
|:----:|:----------------|:-------------------|:----------|
|1     |FL_DATE          |`Date` (YYYY-MM-DD) |Flight Date |
|2     |OP_CARRIER       |`String`            |Unique Carrier Code. When the same code has been used by multiple carriers, a numeric suffix is used for earlier users, for example, PA, PA(1), PA(2). Use this field for analysis across a range of years. |
|3     |OP_CARRIER_FL_NUM|`Integer`           |An identification number assigned by US DOT to identify a unique airline (carrier). A unique airline (carrier) is defined as one holding and reporting under the same DOT certificate regardless of its Code, Name, or holding company/corporation.|
|4     |ORIGIN           |`String`            |Origin Airport|
|5     |DEST             |`String`            |Destination Airport|
|6     |CRS_DEP_TIME     |`Integer` (hhmm)    |CRS Departure Time (local time: hhmm) |
|7     |DEP_TIME         |`Integer` (hhmm)    |Actual Departure Time (local time: hhmm)|
|8     |DEP_DELAY        |`Integer`           |Difference in minutes between scheduled and actual departure time. Early departures show negative numbers.|
|9     |TAXI_OUT         |`Integer` (hhmm)    |Taxi Out Time, in Minutes|
|10    |WHEELS_OFF       |`Integer` (hhmm)    |Wheels Off Time (local time: hhmm)|
|11    |WHEELS_ON        |`Integer` (hhmm)    |Wheels On Time (local time: hhmm)|
|12    |TAXI_IN          |`Integer` (hhmm)    |Taxi In Time, in Minutes|
|13    |CRS_ARR_TIME     |`Integer` (hhmm)    |CRS Arrival Time (local time: hhmm)|
|14    |ARR_TIME         |`Integer` (hhmm)    |Actual Arrival Time (local time: hhmm)|
|15    |ARR_DELAY        |`Integer`           |Difference in minutes between scheduled and actual arrival time. Early arrivals show negative numbers.|
|16    |CANCELLED        |`Integer` (0,1)     |Cancelled Flight Indicator (1=Yes)|
|17    |CANCELLATION_CODE|`Char` (A,B,C,D)    |Specifies The Reason For Cancellation, A:Carrier, B:Weather, C:National Air System, D:Security|
|18    |DIVERTED         |`Integer` (0,1)     |Diverted Flight Indicator (1=Yes)|
|19    |CRS_ELAPSED_TIME |`Integer`           |CRS Elapsed Time of Flight, in Minutes|
|20    |ACTUAL_ELAPSED_TIME|`Integer`           |Elapsed Time of Flight, in Minutes|
|21    |AIR_TIME         |`Integer`           |Flight Time, in Minutes|
|22    |DISTANCE         |`Integer`           |Distance between airports (miles)|
|23    |CARRIER_DELAY    |`Integer`           |Carrier Delay, in Minutes|
|24    |WEATHER_DELAY    |`Integer`           |Weather Delay, in Minutes|
|25    |NAS_DELAY        |`Integer`           |National Air System Delay, in Minutes|
|26    |SECURITY_DELAY   |`Integer`           |Security Delay, in Minutes|
|27    |LATE_AIRCRAFT_DELAY|`Integer`           |Late Aircraft Delay, in Minutes|

## Samples
- **Total Samples**: 68,979,001
- **Total Files**: 11

## Train Dataset
- **Total Samples**: 121,513
- **Years**: `2009`, `2010`, `2011`, `2012`, `2013`, `2014`, `2015`, `2016`, `2017`, `2018`, `2019`
- **Sample Number of Years**:
  |2009|2010|2011|2012|2013|2014|2015|2016|2017|2018|
  |:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
  |12,819|12,870|11,851|12,065|12,673|11,250|11,337|11,246|11,353|14,049|
  ![alt](img/Trainset-Count-Year.png)
