# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import geopandas
import plotly.graph_objs as go
import pandas as pd

import json
#load pandas data framework
# Load and Convert GeoJSON file
#gdf = geopandas.read_file('al152017_fcst_latest')
dfH = pd.read_csv('MARIA-2017 Atlantic Basin.csv')

#sources=[{"type": "FeatureCollection", 'features': [feat]} for feat in geoj2['features']]
mapbox_access_token='pk.eyJ1IjoibnZvc3MxMjgzOCIsImEiOiJjajgwbnowdW4yMWNmMnlvMmlhYWUza3J3In0.P2q3gFkKl5MRAdn4brhE_A'
scl = [0,"rgb(150,0,90)"],[0.125,"rgb(0, 0, 200)"],[0.25,"rgb(0, 25, 255)"],\
[0.375,"rgb(0, 152, 255)"],[0.5,"rgb(44, 255, 150)"],[0.625,"rgb(151, 255, 0)"],\
[0.75,"rgb(255, 234, 0)"],[0.875,"rgb(255, 111, 0)"],[1,"rgb(255, 0, 0)"]
data = go.Data([
    go.Scattermapbox(
        lat=['%s'%(18+28.0/60.0)],
        lon=['%s'%(-66 -  42.1/60.0)],
        mode='markers',
        text=['Tide Guage']
    ),
    go.Scattermapbox(
        lat = dfH['Latitude'].values,
        lon = dfH['Longitude'].values,
        text = [str(v) + ' knts' for v in dfH['Max Winds']],
        marker = dict(
            color = dfH['Max Winds'].values,
            colorscale = scl,
            size=20,
            colorbar = dict(
                thickness = 10,
                titleside = "right",
                outlinecolor = "rgba(68, 68, 68, 0)",
                ticks = "outside",
                ticklen = 3,
                showticksuffix = "last",
                ticksuffix = " kts",
                dtick = 20
            ),
        ),
    )
])

layout = go.Layout(
    height=800,
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=(18+28.0/60.0),
            lon=(-66 -  42.1/60.0)
        ),
        pitch=0,
        zoom=5,
        style='light'
    ),
)
figMap = dict(data=data, layout=layout)
app = dash.Dash()
dfWl = pd.read_csv('CO-OPS__9757809__wl.csv')
dfPr = pd.read_csv('CO-OPS__9757809__pr.csv')
dfRain = pd.read_table('prec.txt',comment='#')
dfRain.drop(dfRain.index[0], inplace=True)
app.layout = html.Div(children=[
    html.H1(children='Hurricane Maria'),

    html.Div(children='''
        An exploration of Hurrican Maria Data.
    '''),
    html.Div([
    dcc.Graph(
        id='tide-gauge',
        figure={
            'data': [
                {'x': dfWl['Date Time'], 'y':dfWl[' Water Level'], 'type': 'scatter', 'name': 'Water Level'},
                {'x': dfPr['Date Time'], 'y':dfPr[' Prediction'], 'type': 'scatter', 'name': 'Predicted'}
            ],
            'layout': {
                'title': 'Tide Guage Aricebo,PR'
            }
        },
    )],style={'width': '48%', 'display': 'inline-block'}),
    html.Div([
    dcc.Graph(
        id='precipition',
        figure={
            'data': [
                {'x': dfRain['datetime'], 'y':dfRain['123882_00045'], 'type': 'scatter', 'name': 'Water Level'}

            ],
            'layout': go.Layout(
                xaxis={ 'title': 'Date'},
                yaxis={'title': 'Inches'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        },
    )],style={'width': '48%', 'display': 'inline-block','float':'right'}),
    html.Div([
        dcc.Graph(id='Map',figure=figMap)
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
