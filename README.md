![alt](./imgs/UoN_Primary_Logo_RGB.png)
# :large_orange_diamond:COMP4107 Big Data Coursework Group 2

## :large_blue_diamond:Introduction
This is the repository for UNNC Big Data Coursework Group 2`(COMP4107)`.

The course information are:
- **Big Data**
- COMP4107
- UNNC 2023 Final Year Module

The members of the `group 2` are:
- :student:**Ran JI** 20217337
  :mailbox:scyrj1@nottingham.edu.cn
- :student:**Yik LAU** 20217531
  :mailbox:scyyl18@nottingham.edu.cn
- :student:**Jiarui LI** 20216422 `Group Leader`
  :mailbox:scyjl6@nottingham.edu.cn

This coursework is supervised by:

:man_teacher:Professor Zheng LU.

## :large_blue_diamond:Topic
Preference ranking:
- :green_circle::bookmark:**BD07** An Optimised Classification for Flight Status
- :bookmark:**BD09** Analysis the Impact of Green Infrastructure on Carbon Monoxide Reduction
- :bookmark:**BD05** Climate Change Analysis in Brazil


Final decision: :bookmark:**BD07** `An Optimised Classification for Flight Status`

## :large_blue_diamond:TO DO
```mermaid
gitGraph
    commit id: "Init Project"
    commit id: "Group Create"
    commit id: "Git Repository Create"
    commit id: "Topic Selection Email Sent"
    commit id: "Topic Confirm BD 07"
```
- [ ] :hourglass:Topic Preparing
  - [x] Send Topic Choose Email
  - [x] Confirm Topic
  - [ ] Collect Topic Basic Information
  - [x] Team GitHub Init
  - [x] Team Chat Group Init

## :large_blue_diamond:Documents
### :small_blue_diamond:Coursework Specification
:file_folder:[Coursework for COMP4107 Big Data.pdf](./docs/Coursework%20for%20COMP4107%20Big%20Data.pdf) `Update: 2023/04/08`
### :small_blue_diamond:Templates
#### Report Template
:file_folder:[Conference-LaTeX-template.zip](./docs/Templates/Conference-LaTeX-template.zip) `Update: 2023/04/08` `LaTeX`

Related Document: :file_folder:[IEEEtran_HOWTO.pdf](./docs/Templates/IEEEtran_HOWTO.pdf)

#### Representation Slide Template
:file_folder:[CW presenation -Template.pptx](./docs/Templates/CW%20presenation%20-Template.pptx) `Update: 2023/04/08` `pptx`

### :small_blue_diamond:Cheatsheet
- :spiral_notepad:[Spark Cheatsheet](https://www.datacamp.com/cheat-sheet/pyspark-cheat-sheet-spark-in-python)
- :spiral_notepad:[Python Cheatsheet](https://www.pythoncheatsheet.org/)
- :spiral_notepad:[Pandas Cheatsheet](https://www.datacamp.com/cheat-sheet/pandas-cheat-sheet-for-data-science-in-python)
- :spiral_notepad:[Numpy Cheatsheet](https://www.datacamp.com/cheat-sheet/numpy-cheat-sheet-data-analysis-in-python)
- :spiral_notepad:[Matplotlib Cheatsheet](https://matplotlib.org/cheatsheets/)
- :spiral_notepad:[PyTorch Cheatsheet](https://pytorch.org/tutorials/beginner/ptcheat.html)
### :small_blue_diamond:Documentation
- :notebook:[Python Documentation `3.11.3`](https://docs.python.org/3/)
- :notebook:[Spark Documentation `3.3.2`](https://spark.apache.org/docs/latest/)
- :notebook:[PyTorch Documentation `2.0`](https://pytorch.org/docs/stable/index.html)

### :small_blue_diamond:Resource
#### ICON
- :framed_picture:[UNNC ICON](./imgs/UoN_Primary_Logo_RGB.png)


## :large_blue_diamond:Dataset
### :package: Airline Delay Analysis
#### :link: Dataset Link
- [:link: Kaggle Dataset <img src="https://www.kaggle.com/static/images/site-logo.svg" width="50">](https://www.kaggle.com/datasets/sherrytp/airline-delay-analysis)
- [:link: BTS (Original Dataset) <img src="https://www.transtats.bts.gov/images/smalltop.gif" width="85">](https://www.transtats.bts.gov/Tables.asp?DB_ID=120&DB_Name=Airline%20On-Time%20Performance%20Data&DB_Short_Name=On-Time)
#### Introduction
The datasets contain daily airline information covering from flight information, carrier company, to taxing-in, taxing-out time, and generalized delay reason of exactly 10 years, from 2009 to 2019. The DOT's database is renewed from 2018, so there might be a minor change in the column names.

#### Files
- :open_file_folder: airline delay analysis `2GB`
  - :spiral_notepad: 20.csv `266.95MB`
  - :spiral_notepad: 2009.csv
  - :spiral_notepad: 2010.csv
  - :spiral_notepad: 2011.csv
  - :spiral_notepad: 2012.csv
  - :spiral_notepad: 2013.csv
  - :spiral_notepad: 2014.csv
  - :spiral_notepad: 2015.csv
  - :spiral_notepad: 2016.csv
  - :spiral_notepad: 2017.csv
  - :spiral_notepad: 2018.csv
  - :spiral_notepad: 2019.csv
#### Dataset Schema
|Column|Table Token      |Type                |Description|
|:----:|:----------------|:-------------------|:----------|
|1     |FL_DATE          |`Date` (YYYY-MM-DD) |Flight Date |
|2     |OP_CARRIER       |`String`            |Unique Carrier Code. When the same code has been used by multiple carriers, a numeric suffix is used for earlier users, for example, PA, PA(1), PA(2). Use this field for analysis across a range of years. |
|3     |OP_CARRIER_FL_NUM|`Integer`           |An identification number assigned by US DOT to identify a unique airline (carrier). A unique airline (carrier) is defined as one holding and reporting under the same DOT certificate regardless of its Code, Name, or holding company/corporation.|
|4     |ORIGIN           |`String`            |Origin Airport|
|5     |DEST             |`String`            |Destination Airport|
|6     |CRS_DEP_TIME     |`Integer` (hhmm)    |CRS Departure Time (local time: hhmm) |
|7     |DEP_TIME         |`Float`             |Actual Departure Time (local time: hhmm)|
|8     |DEP_DELAY        |`Float`             |Difference in minutes between scheduled and actual departure time. Early departures show negative numbers.|
|9     |TAXI_OUT         |`Integer` (hhmm)    |Taxi Out Time, in Minutes|
|10    |WHEELS_OFF       |`Integer` (hhmm)    |Wheels Off Time (local time: hhmm)|
|11    |WHEELS_ON        |`Float`             |Wheels On Time (local time: hhmm)|
|12    |TAXI_IN          |`Integer` (hhmm)    |Taxi In Time, in Minutes|
|13    |CRS_ARR_TIME     |`Float`             |CRS Arrival Time (local time: hhmm)|
|14    |ARR_TIME         |`Float`             |Actual Arrival Time (local time: hhmm)|
|15    |ARR_DELAY        |`Float`             |Difference in minutes between scheduled and actual arrival time. Early arrivals show negative numbers.|
|16    |CANCELLED        |`Integer` (0,1)     |Cancelled Flight Indicator (1=Yes)|
|17    |CANCELLATION_CODE|`Char` (A,B,C,D)    |Specifies The Reason For Cancellation, A:Carrier, B:Weather, C:National Air System, D:Security|
|18    |DIVERTED         |`Integer` (0,1)     |Diverted Flight Indicator (1=Yes)|
|19    |CRS_ELAPSED_TIME |`Float`             |CRS Elapsed Time of Flight, in Minutes|
|20    |ACTUAL_ELAPSED_TIME|`Float`             |Elapsed Time of Flight, in Minutes|
|21    |AIR_TIME         |`Float`             |Flight Time, in Minutes|
|22    |DISTANCE         |`Float`             |Distance between airports (miles)|
|23    |CARRIER_DELAY    |`Float`             |Carrier Delay, in Minutes|
|24    |WEATHER_DELAY    |`Float`             |Weather Delay, in Minutes|
|25    |NAS_DELAY        |`Float`             |National Air System Delay, in Minutes|
|26    |SECURITY_DELAY   |`Float`             |Security Delay, in Minutes|
|27    |LATE_AIRCRAFT_DELAY|`Float`             |Late Aircraft Delay, in Minutes|

#### Related Datasheet
- Airport Code Explanation: `CSV` [:spiral_notepad: L_AIRPORT.csv](./datasets/L_AIRPORT.csv)


## :large_blue_diamond:Methods
_wait for topic confirm_
## :large_blue_diamond:Reports
_wait for topic confirm_


<div style="padding: 1rem; border-radius: 10pt;">
  <a href="https://www.python.org/">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1200px-Python-logo-notext.svg.png" width="30">
  </a>
  <a href="https://spark.apache.org/">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Apache_Spark_logo.svg/1200px-Apache_Spark_logo.svg.png" width="70">
  </a>
  <a href="https://numpy.org/">
    <img src="https://numpy.org/images/logo.svg" width="40">
  </a>
  <a href="https://www.kaggle.com/">
    <img src="https://www.kaggle.com/static/images/site-logo.svg" width="70">
  </a>
</div>