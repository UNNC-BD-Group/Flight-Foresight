import streamlit as st
import pandas as pd
from datetime import date
import plotly.graph_objects as go
import numpy as np

@st.cache_resource
def load_airline_data(path='./'):
    return pd.read_csv(path)

def get_airport_list(dataframe, airport_path='../datasets/AIRPORTS_INFO.csv'):
    dest_airports = dataframe['DEST'].unique()
    airports_info = pd.read_csv(airport_path)
    dest_airports_info = []
    for line in airports_info.values:
        if line[14] in dest_airports:
            dest_airports_info.append(line)
    return pd.DataFrame(dest_airports_info, columns=airports_info.columns)

def get_airport(code, airport_path='../datasets/AIRPORTS_INFO.csv'):
    airports_info = pd.read_csv(airport_path)
    for line in airports_info.values:
        if line[14] == code:
            return line

def get_airport_selection_list(airport_list):
    select_list = []
    for item in airport_list.values:
        select_list.append('{}, [{}]{}, {}'.format(item[14], item[9], item[3], item[10]))
    return select_list

hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

flight_date = st.sidebar.date_input('Flight Date', value=date(2019, 1, 1), min_value=date(2019, 1, 1), max_value=date(2019, 12, 31))

airline_dataframe = load_airline_data('../datasets/airline-delay-analysis/2019.csv')
airport_list = get_airport_list(airline_dataframe[airline_dataframe['FL_DATE'] == '{}-{:0>2d}-{:0>2d}'.format(flight_date.year, flight_date.month, flight_date.day)][airline_dataframe['ARR_TIME'].notna()], '../datasets/AIRPORTS_INFO.csv')

option = st.sidebar.selectbox('Airport', get_airport_selection_list(airport_list))

airport = option[:3]
airport_info = airport_list[airport_list['iata_code'] == airport].values[0]
st.sidebar.title('{}'.format(airport_info[3]))
cols = st.sidebar.columns(3)
cols[0].metric('IATA', airport)
cols[1].metric('Country', airport_info[9].split('-')[0])
cols[2].metric('Region', airport_info[9].split('-')[1])
st.sidebar.write('{:.4f}, {:.4f}'.format(airport_info[4], airport_info[5]))
st.sidebar.map(pd.DataFrame([[airport_info[4], airport_info[5]]], columns=['lat', 'lon']))

st.image('./bar-img.png')

cols = st.columns(2)
cols[0].header('✈️{}'.format(airport))
cols[0].write(airport_info[3])

flights_table = airline_dataframe[airline_dataframe['FL_DATE'] == '{}-{:0>2d}-{:0>2d}'.format(flight_date.year, flight_date.month, flight_date.day)]
flights_table = flights_table[airline_dataframe['DEST']==airport]
flights_table = flights_table[airline_dataframe['ARR_TIME'].notna()]
flights_table = flights_table.sort_values('ARR_TIME')
flight_list = flights_table[['OP_CARRIER', 'OP_CARRIER_FL_NUM', 'ORIGIN', 'ARR_TIME', 'ARR_DELAY']].values

# flight_table = []
# rows = []
# for line in flight_list:
#     arr = '{:0>2d}:{:0>2d}'.format(int(line[3]/100), int(line[3]%100))
#     arr_status = ''
#     if line[4] == 0:
#         arr_status = 'On Plan'
#     elif line[4] < 0:
#         arr_status = 'Ahead'
#     else:   
#          arr_status = 'Delay'
#     flight_table.append([line[2], arr, arr_status])
#     rows.append('{}{}'.format(line[0], line[1]))
# flight_table = pd.DataFrame(flight_table, columns=['From', 'Expect', 'Estimate'], index=rows)
# cols[0].table(flight_table)
lines = '|Flight|From|Expect|Estimate|\n|:--|:--:|:--:|:--|\n'
delay_count = 0
ahead_count = 0
onplan_count = 0
flight_num_list = []
for line in flight_list:
    arr = '{:0>2d}:{:0>2d}'.format(int(line[3]/100), int(line[3]%100))
    arr_status = ''
    if line[4] == 0:
        arr_status = ':green[On Plan]'
        onplan_count += 1
    elif line[4] < 0:
        arr_status = ':blue[Ahead]'
        ahead_count += 1
    else:   
         arr_status = ':red[Delay]'
         delay_count += 1
    flight_num = '{}{}'.format(line[0], line[1])
    flight_num_list.append(flight_num)
    lines += ('|🛬**{}**|`{}`|{}|{}|\n'.format(flight_num, line[2], arr, arr_status))
    
status_bar = cols[0].columns(4)
status_bar[0].metric('Total', '{}'.format(delay_count+ahead_count+onplan_count))
status_bar[1].metric(':red[Delay]', '{}'.format(delay_count))
status_bar[2].metric(':blue[Ahead]', '{}'.format(ahead_count))
status_bar[3].metric(':green[OnPlan]', '{}'.format(onplan_count))
cols[0].markdown(lines)

flight_num = cols[1].selectbox('Flight', flight_num_list)
flight_num_full = flight_num
carrier = flight_num[:2]
flight_num = flight_num[2:]


flight_info = flights_table[flights_table['OP_CARRIER_FL_NUM']==int(flight_num)].values[0]

origin_airport_info = get_airport(flight_info[3], '../datasets/AIRPORTS_INFO.csv')

cols[1].markdown('🛫**{:0>2d}:{:0>2d}** **{}** - {}'.format(
    int(flight_info[5]/100), int(flight_info[5]%100),
    origin_airport_info[14],
    origin_airport_info[3]
    ))
# cols[1].markdown('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**↧**')
cols[1].markdown('🛬**{:0>2d}:{:0>2d}** **{}** - {}'.format(
    int(flight_info[11]/100), int(flight_info[11]%100),
    airport,
    airport_info[3],
    ))

flight_status = cols[1].columns(3)
flight_status[0].metric('From', flight_info[3])
flight_status[1].metric('Expect', '{:0>2d}:{:0>2d}'.format(int(flight_info[11]/100), int(flight_info[11]%100)))

arr_delay = flight_info[12]
if arr_delay == 0:
    flight_status[2].metric(':green[On Plan]', 'Accurate')
elif arr_delay < 0:
    flight_status[2].metric(':blue[Ahead]', '{:.0f} min'.format(abs(arr_delay)))
else:
    flight_status[2].metric(':red[Delay]', '{:.0f} min'.format(abs(arr_delay)))

cols[1].map(pd.DataFrame([[origin_airport_info[4], origin_airport_info[5]]], columns=['lat', 'lon']))