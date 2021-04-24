import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_html_components as html
from dash.dependencies import Input, Output
import random
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go

Gauge_width    = 240
Gauge_height   = 180
Gauge_margins  = 30
Gauge_margins2 = 0

data = {'Date' : range(0,100),
        'T1': [random.uniform(10,40) for _ in range(100)],
        'T2': [random.uniform(10,40) for _ in range(100)],
        'T3': [random.uniform(10,40) for _ in range(100)],
        'H1': [random.uniform(10,100) for _ in range(100)],
        'H2': [random.uniform(10,100) for _ in range(100)],
        'H3': [random.uniform(10,100) for _ in range(100)],
        'L1': [bool(random.getrandbits(1)) for _ in range(100)],
        'L2': [bool(random.getrandbits(1)) for _ in range(100)],
        'R3': [bool(random.getrandbits(1)) for _ in range(100)],
        'R4': [bool(random.getrandbits(1)) for _ in range(100)],
        'R5': [bool(random.getrandbits(1)) for _ in range(100)],
        'R6': [bool(random.getrandbits(1)) for _ in range(100)]
        }

#df = pd.DataFrame (data)
df = pd.read_csv('log.csv') 

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    
    dbc.Row(
    [
        dbc.Col(html.Div(dcc.Graph('t1-gauge')),style={'display': 'inline-block'}),
        dbc.Col(html.Div(dcc.Graph('t2-gauge')),style={'display': 'inline-block'}),
        dbc.Col(html.Div(dcc.Graph('t3-gauge')),style={'display': 'inline-block'}),
        dbc.Col(html.Div(dcc.Graph('h1-gauge')),style={'display': 'inline-block'}),
        dbc.Col(html.Div(dcc.Graph('h2-gauge')),style={'display': 'inline-block'}),

        dbc.Col(html.Div(daq.Indicator(id='l1-ind',label="Light 1"    ,width=60,height=150,color="#FFFF00",style={'width': '120px','margin-top': 0,'margin-bottom': -10})),style={'display': 'inline-block'}),
        dbc.Col(html.Div(daq.Indicator(id='l2-ind',label="Light 2"    ,width=60,height=150,color="#FFFF00",style={'width': '120px','margin-top': 0,'margin-bottom': -10})),style={'display': 'inline-block'}),
        dbc.Col(html.Div(daq.Indicator(id='tapp-ind',label="Tappetino",width=60,height=150,color="#FF0000",style={'width': '120px','margin-top': 0,'margin-bottom': -10})),style={'display': 'inline-block'}),

        dbc.Col(html.Div([dcc.Dropdown(id='time_sel', options=[{'label': i, 'value': i} for i in ["6h","24h","1w"]],value='24h', style={'width': '100px'})] ),style={'display': 'inline-block'}),
    ]),
    
    dcc.Graph('temp-graph', config={'displayModeBar': False},style={'height': '400px','margin-top': 0,'margin-bottom': -100}),
    dcc.Graph('hum-graph' , config={'displayModeBar': False},style={'height': '400px','margin-top': 0,'margin-bottom': -100}),
    
    dcc.Interval(id='interval-component1',interval=1*1000,n_intervals=0),
    dcc.Interval(id='interval-component2',interval=1*1000,n_intervals=0)
    
    ])

#Temperature graph
@app.callback(
    Output('temp-graph', 'figure'),
    [Input('time_sel', 'value')]
)
def update_graph(grpname):
    return px.line(df, x='Date', y=['T1', 'T2', 'T3'])

#Humidity graph
@app.callback(
    Output('hum-graph', 'figure'),
    [Input('time_sel', 'value')]
)
def update_graph(grpname):
    return px.line(df, x='Date', y=['H1', 'H2'], labels=['H1', 'H2'])

#T1 gauge
@app.callback(
    Output('t1-gauge', 'figure'),
    [Input('interval-component1', 'n_intervals')]
)
def update_graph(grpname):
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = df["T1"].iloc[-1],
        mode = "gauge+number",
        title = {'text': "T1"},
        # delta = {'reference': 380},
        gauge = {'axis': {'range': [10, 40]},
                # 'steps' : [
                    # {'range': [0, 250], 'color': "lightgray"},
                    # {'range': [250, 400], 'color': "gray"}],
                'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 490}
                }
                ))
    fig.update_layout(autosize=False,width=Gauge_width,height=Gauge_height,margin=dict(l=Gauge_margins, r=Gauge_margins, t=Gauge_margins2, b=Gauge_margins2))
    return fig

#T2 gauge
@app.callback(
    Output('t2-gauge', 'figure'),
    [Input('interval-component2', 'n_intervals')]
)
def update_graph(grpname):
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = df["T2"].iloc[-1],
        mode = "gauge+number",
        title = {'text': "T2"},
        # delta = {'reference': 380},
        gauge = {'axis': {'range': [10, 40]},
                # 'steps' : [
                    # {'range': [0, 250], 'color': "lightgray"},
                    # {'range': [250, 400], 'color': "gray"}],
                'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 490}
                }
                ))
    fig.update_layout(autosize=False,width=Gauge_width,height=Gauge_height,margin=dict(l=Gauge_margins, r=Gauge_margins, t=Gauge_margins2, b=Gauge_margins2))
    return fig

#T3 gauge
@app.callback(
    Output('t3-gauge', 'figure'),
    [Input('interval-component2', 'n_intervals')]
)
def update_graph(grpname):
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = df["T3"].iloc[-1],
        mode = "gauge+number",
        title = {'text': "T3"},
        # delta = {'reference': 380},
        gauge = {'axis': {'range': [10, 40]},
                # 'steps' : [
                    # {'range': [0, 250], 'color': "lightgray"},
                    # {'range': [250, 400], 'color': "gray"}],
                'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 490}
                }
                ))
    fig.update_layout(autosize=False,width=Gauge_width,height=Gauge_height,margin=dict(l=Gauge_margins, r=Gauge_margins, t=Gauge_margins2, b=Gauge_margins2))
    return fig

#H1 gauge
@app.callback(
    Output('h1-gauge', 'figure'),
    [Input('interval-component1', 'n_intervals')]
)
def update_graph(grpname):
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = df["H1"].iloc[-1],
        mode = "gauge+number",
        title = {'text': "H1"},
        # delta = {'reference': 380},
        gauge = {'axis': {'range': [30, 100]},
                # 'steps' : [
                    # {'range': [0, 250], 'color': "lightgray"},
                    # {'range': [250, 400], 'color': "gray"}],
                'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 490}
                }
                ))
    fig.update_layout(autosize=False,width=Gauge_width,height=Gauge_height,margin=dict(l=Gauge_margins, r=Gauge_margins, t=Gauge_margins2, b=Gauge_margins2))
    return fig

#H2 gauge
@app.callback(
    Output('h2-gauge', 'figure'),
    [Input('interval-component1', 'n_intervals')]
)
def update_graph(grpname):
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = df["H2"].iloc[-1],
        mode = "gauge+number",
        title = {'text': "H2"},
        # delta = {'reference': 380},
        gauge = {'axis': {'range': [30, 100]},
                # 'steps' : [
                    # {'range': [0, 250], 'color': "lightgray"},
                    # {'range': [250, 400], 'color': "gray"}],
                'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 490}
                }
                ))
    fig.update_layout(autosize=False,width=Gauge_width,height=Gauge_height,margin=dict(l=Gauge_margins, r=Gauge_margins, t=Gauge_margins2, b=Gauge_margins2))
    # fig.update_yaxes(automargin=True)
    return fig

#L1 ind
@app.callback(
    Output('l1-ind', 'color'),
    [Input('interval-component1', 'n_intervals')]
)
def update_graph(grpname):
    if bool(random.getrandbits(1)):
        return "#FFFF00"
    else:
        return "#000000"	

#L2 ind
@app.callback(
    Output('l2-ind', 'color'),
    [Input('interval-component1', 'n_intervals')]
)
def update_graph(grpname):
    if bool(random.getrandbits(1)):
        return "#FFFF00"
    else:
        return "#000000"	

#tapp ind
@app.callback(
    Output('tapp-ind', 'color'),
    [Input('interval-component1', 'n_intervals')]
)
def update_graph(grpname):
    if bool(random.getrandbits(1)):
        return "#FF0000"
    else:
        return "#000000"	


if __name__ == '__main__':
    app.run_server(host= '0.0.0.0',debug=True)
    #app.run_server(debug=True)
