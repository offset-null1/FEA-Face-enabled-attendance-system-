import numpy as np
import pandas as pd

import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from .data import create_dataframe
from .layout import html_layout


def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=[
            '/static/dist/css/styles.css',
        ]
    )

    # Create Dash Layout
    dash_app.layout = html.Div(id='dash-container')
    init_callbacks(dash_app)
    
    return dash_app.server

def init_callbacks(dash_app):
    @app.callbacks(...)
    def update_graph(rows):
        ...
    
    
def create_data_table(df):
    table = dash_table.DataTable(...)
    return table