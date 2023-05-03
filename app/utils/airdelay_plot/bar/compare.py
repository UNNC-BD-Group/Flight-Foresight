import plotly.graph_objects as go

def method_compare(log):
    train_rmse = [log[i]['train']['rmse'] for i in log]
    test_rmse = [log[i]['test']['rmse'] for i in log]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=list(log.keys()),
                    y=list(train_rmse),
                    texttemplate='%{customdata}',
                    customdata=['{:.2f}'.format(i) for i in train_rmse],
                    name='Train RMSE',
                    marker_color='rgb(55, 83, 109)',
                    width=0.25
                    ))
    fig.add_trace(go.Bar(x=list(log.keys()),
                    y=list(test_rmse),
                    texttemplate='%{customdata}',
                    customdata=['{:.2f}'.format(i) for i in test_rmse],
                    name='Test RMSE',
                    marker_color='rgb(26, 118, 255)',
                    width=0.25
                    ))
    fig.update_layout(
        title='Method Root Mean Square Error Comparison',
        height=500,
        width=700,
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='RMSE',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        bargap=0.05,
        xaxis_tickangle=-45
    )
    return fig