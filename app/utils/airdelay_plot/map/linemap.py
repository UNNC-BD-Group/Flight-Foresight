import plotly.graph_objects as go
import numpy as np

def linemap(airdelay_dataframe, color='royalblue', name='', fig=None):
    if fig is None:
        fig = go.Figure()
        
    frame = airdelay_dataframe
    frame = frame.dataframe('spark')
    frame = frame.groupBy('ORIGIN', 'DEST').count().orderBy('count')
    frame = airdelay_dataframe.derive(frame)
    frame = frame.attach_airport_info('both').dataframe('pandas')
    
    lons = np.empty(3 * len(frame))
    lons[::3] = frame['ORIGIN_LON']
    lons[1::3] = frame['DEST_LON']
    lons[2::3] = None
    
    lats = np.empty(3 * len(frame))
    lats[::3] = frame['ORIGIN_LAT']
    lats[1::3] = frame['DEST_LAT']
    lats[2::3] = None
    
    fig.add_trace(
        go.Scattergeo(
            lon = lons,
            lat = lats,
            mode = 'lines',
            line = dict(width = 0.5,color = color),
            opacity = 0.5,
            name=name
        )
    )
    
    fig.add_trace(go.Scattergeo(
    lon = frame['ORIGIN_LON'],
    lat = frame['ORIGIN_LAT'],
    hoverinfo = ['text', 'lon', 'lat'],
    text = frame['ORIGIN_REGION'],
    mode = 'markers',
    name = '',
    marker = dict(
        size = 1,
        color = color
    )))
    
    fig.add_trace(go.Scattergeo(
    lon = frame['DEST_LON'],
    lat = frame['DEST_LAT'],
    hoverinfo = ['text', 'lon', 'lat'],
    text = frame['DEST_REGION'],
    mode = 'markers',
    name = '',
    marker = dict(
        size = 1,
        color = color
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
    
    