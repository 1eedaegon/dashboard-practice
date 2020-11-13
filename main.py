# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from preprocess import CoronaPreprocess
from elements_builder import make_table, make_map, make_bar, make_line

# Initialize preprocessor
preprocess = CoronaPreprocess()
preprocess.set_data_repo(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data"
)
preprocess.load_daily_data()
preprocess.load_time_data()
# https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/07-21-2020.csv
# https://raw.githubusercontent.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports/11-09-2020.csv
# Data preprocessing
countries_df = preprocess.start_daily_prep()
total_df = preprocess.start_total_prep()
conditions = preprocess.get_condition()
global_total_df = preprocess.start_time_prep()

options_by_countries = countries_df.sort_values("국가 구분").reset_index()
options_by_countries = options_by_countries["국가 구분"]
# print(options_by_countries)

# Make graph figure using builder
map_fig = make_map(countries_df)
table_fig = make_table(countries_df)
bar_fig = make_bar(total_df, conditions)

bar_fig.update_traces(marker_color=["#e74c3c", "#bdc3c7", "#2ecc71"])

reset_stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.css",
    "https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap",
]

app = dash.Dash(__name__, external_stylesheets=reset_stylesheets)

app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "backgroundColor": "black",
        "color": "white",
        "fontFamily": "Open Sans, serif",
    },
    children=[
        html.Header(
            style={"textAlign": "center", "padding": "40px 0"},
            children=[
                html.Header(
                    style={"textAlign": "center"},
                    children=[html.H1("Corona Dashboard", style={"fontSize": 40})],
                )
            ],
        ),
        html.Div(
            style={
                "display": "grid",
                "gap": 50,
                "gridTemplateColumns": "repeat(4, 1fr)",
            },
            children=[
                html.Div(
                    style={"grid-column": "span 3"},
                    children=[dcc.Graph(figure=map_fig)],
                ),
                html.Div(children=[table_fig]),
            ],
        ),
        html.Div(
            style={
                "display": "grid",
                "gap": 50,
                "gridTemplateColumns": "repeat(4,1fr)",
            },
            children=[
                html.Div(children=[dcc.Graph(figure=bar_fig)]),
                html.Div(
                    style={"grid-column": "span 3"},
                    children=[
                        dcc.Dropdown(
                            id="country",
                            options=[
                                {"label": country, "value": country}
                                for country in options_by_countries
                            ],
                        ),
                        # html.H1(id="country-graph")
                        dcc.Graph(id="country-graph"),
                    ],
                ),
            ],
        ),
    ],
)
# make_bar.update_layout(margin=dict(l=0, r=0, t=50, b=0))


@app.callback(Output("country-graph", "figure"), [Input("country", "value")])
def update_hello(country_name):
    global_total_df = preprocess.start_time_prep()
    if country_name:
        preprocess.set_country(country_name)
        global_total_df = preprocess.start_time_prep_by_country()
        fig = make_line(global_total_df, country_name)
    else:
        fig = make_line(global_total_df)
    return fig


server = app.server

if __name__ == "__main__":
    app.run_server(debug=True)