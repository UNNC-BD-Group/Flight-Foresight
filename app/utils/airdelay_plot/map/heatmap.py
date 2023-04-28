import plotly.graph_objects as go

def heatmap(airdelay_dataframe, port='origin', color='royalblue', name='', fig=None):
    '''
    port = 'origin' | 'dest'
    '''
    frame = airdelay_dataframe
    frame = frame.dataframe('spark')
    
    if port == 'origin':
        frame = frame.groupBy('origin').count().orderBy('count')
        frame = airdelay_dataframe.derive(frame)
        frame = frame.attach_airport_info('origin').dataframe()
        frame = frame.withColumnRenamed('ORIGIN_LAT', 'LAT')
        frame = frame.withColumnRenamed('ORIGIN_LON', 'LON')
        frame = frame.withColumnRenamed('ORIGIN_REGION', 'REGION')
        frame = frame.withColumnRenamed('ORIGIN', 'AIRPORT')
        
    elif port == 'dest':
        frame = frame.groupBy('dest').count().orderBy('count')
        frame = airdelay_dataframe.derive(frame)
        frame = frame.attach_airport_info('dest').dataframe()
        frame = frame.withColumnRenamed('DEST_LAT', 'LAT')
        frame = frame.withColumnRenamed('DEST_LON', 'LON')
        frame = frame.withColumnRenamed('DEST_REGION', 'REGION')
        frame = frame.withColumnRenamed('DEST', 'AIRPORT')
    
    else:
        raise Exception('Unexpected Port Parameter')
    frame = frame.toPandas()
    
    if fig is None:
        fig = go.Figure()
    fig.add_trace(go.Scattergeo(lat=frame['LAT'],
                                 lon=frame['LON'],
                                 text=frame['REGION'],
                                 name=name,
                                 marker = dict(
                                    size = frame['count'],
                                    line_color='rgb(40,40,40)',
                                    line_width=0.5,
                                    sizemode = 'area',
                                    color=color
                                )))
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(
        geo = go.layout.Geo(
            scope = 'north america',
            projection_type = 'azimuthal equal area',
            showland = True,
            landcolor = 'rgb(243, 243, 243)',
            countrycolor = 'rgb(204, 204, 204)',
        )
    )
    
    return fig
    
    
    
    