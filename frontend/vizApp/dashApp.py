import numpy as np
import pandas as pd

import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from .data import create_dataframe
from .layout import html_layout

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=[
            external_stylesheets,
        ]
    )

    # Create Dash Layout
    dash_app.layout = html.Div(id='dash-container')
    # init_callbacks(dash_app)
    create_data_table(dash_app)
    return dash_app.server

# def init_callbacks(dash_app):
#     @app.callbacks(...)
#     def update_graph(rows):
#         ...
    
    
def create_data_table(app):
    df = pd.DataFrame({
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    })

    fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

    app.layout = html.Div(children=[
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for Python.
        '''),

        dcc.Graph(
            id='example-graph',
            figure=fig
        )
    ])
    # table = dash_table.DataTable(...)
    # return table