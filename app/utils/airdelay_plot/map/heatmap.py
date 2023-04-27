import plotly.graph_objects as go

def headmap(airdelay_dataframe, port='origin'):
    '''
    port = 'origin' | 'dest'
    '''
    frame = airdelay_dataframe.attach_airport_info()
    frame = frame.dataframe('spark')
    
    
    