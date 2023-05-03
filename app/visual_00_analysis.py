import streamlit as st
from utils.dataset import AirDelayDataset
from utils import airdelay_plot as plot
import datetime

path = '../datasets/app-dataset/full/train.csv'
airport_path = '../datasets/AIRPORTS_INFO.csv'

@st.cache_resource
def load_data():
    return AirDelayDataset(path, airport_data_path=airport_path)

st.set_page_config(
        page_title='Analysis'
    )

sidebar = st.sidebar
sidebar.title('Airline Delay Each Day')
sidebar.subheader('Change Date')
date_start = sidebar.date_input('Date', datetime.date(2009, 1, 1),
                          datetime.date(2009, 1, 1), datetime.date(2019, 1, 1))
days = sidebar.slider('Day Long', 1, 30, 1)
# days = sidebar.slider('Date', 0, 3651, 0)
# date_start = datetime.date(2009, 1, 1) + datetime.timedelta(days=days)
date_end = date_start + datetime.timedelta(days=days)
date_start = '{}-{:0>2d}-{:0>2d}'.format(date_start.year, date_start.month, date_start.day)
date_end = '{}-{:0>2d}-{:0>2d}'.format(date_end.year, date_end.month, date_end.day)
sidebar.text('{} -> {}'.format(date_start, date_end))

hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

data = load_data()
data = data.get_date_period(date_start, date_end)


st.subheader('Airlines Map')
fig = plot.map.linemap(data, name='Airlines')
fig = plot.map.linemap(data.get_delay(), name='Delay', color='red', fig=fig)
st.plotly_chart(fig)
cols = st.columns(2)
cols[0].text('All Airlines')
d = data.count_airline()
cols[0].text('total: {}'.format(len(d)))
cols[0].dataframe(d)
cols[1].text('Delay')
d = data.get_delay().count_airline()
cols[1].text('total: {}'.format(len(d)))
cols[1].dataframe(d)

st.subheader('Origin Airport Map')
fig = plot.map.heatmap(data, port='origin', name='Origin')
fig = plot.map.heatmap(data.get_delay(), port='origin', name='Delay', color='red', fig=fig)
st.plotly_chart(fig)
cols = st.columns(2)
cols[0].text('Airports')
d = data.count_airport()
cols[0].text('total: {}'.format(len(d)))
cols[0].dataframe(d)
cols[1].text('Delay')
d = data.get_delay().count_airport()
cols[1].text('total: {}'.format(len(d)))
cols[1].dataframe(d)

st.subheader('Destination Airport Map')
fig = plot.map.heatmap(data, port='dest', name='Origin')
fig = plot.map.heatmap(data.get_delay(), port='dest', name='Delay', color='red', fig=fig)
st.plotly_chart(fig)
cols = st.columns(2)
cols[0].text('Airports')
d = data.count_airport()
cols[0].text('total: {}'.format(len(d)))
cols[0].dataframe(d)
cols[1].text('Delay')
d = data.get_delay().count_airport()
cols[1].text('total: {}'.format(len(d)))
cols[1].dataframe(d)