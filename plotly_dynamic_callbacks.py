#This code uses dynamic callback feature to compare various covid kpis across Indian States
import dash  # version 1.13.1
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
import plotly.express as px
import pandas as pd
import numpy as np

df = pd.read_csv(r"https://api.covid19india.org/csv/latest/state_wise.csv")

app = dash.Dash(__name__)
server = app.server
app.layout = html.Div([
html.H2("India Covid Comparison among States using Dynamic Callback", style={'text-align': 'center'}),
    html.Div(children=[
        html.Button('Add Chart', id='add-chart', n_clicks=0),
    ]),
    html.Div(id='container', children=[])
])


@app.callback(
    Output('container', 'children'),
    [Input('add-chart', 'n_clicks')],
    [State('container', 'children')]
)
def display_graphs(n_clicks, div_children):
    new_child = html.Div(
        style={'width': '45%', 'display': 'inline-block', 'outline': 'thin lightgrey solid', 'padding': 10},
        children=[
            dcc.Graph(
                id={
                    'type': 'dynamic-graph',
                    'index': n_clicks
                },
                figure={}
            ),
            dcc.Dropdown(
                id={
                    'type': 'dynamic-dpn-state',
                    'index': n_clicks
                },
                options=[{'label': i, 'value': i} for i in np.sort(df['State'].unique())],
                multi=True,

                placeholder="Select State(s)",
            ),
            dcc.Dropdown(
                id={
                    'type': 'dynamic-dpn-kpi',
                    'index': n_clicks
                },
                options=[{'label': c, 'value': c} for c in ['Confirmed', 'Recovered', 'Deaths','Active']],
                value='Active',
                clearable=False
            )

        ]
    )
    div_children.append(new_child)
    return div_children


@app.callback(
    Output({'type': 'dynamic-graph', 'index': MATCH}, 'figure'),
    [Input(component_id={'type': 'dynamic-dpn-state', 'index': MATCH}, component_property='value'),
     Input(component_id={'type': 'dynamic-dpn-kpi', 'index': MATCH}, component_property='value')
]
)
def update_graph(select_state, select_kpi):
    if select_state is None:
        fig = {}
    else:

        df_temp = df[df['State'].isin(list(select_state))]
        df_temp2 = df_temp[df_temp.columns[:5]]
        final_df = pd.melt(df_temp2, id_vars=['State'], value_vars=select_kpi, var_name='covid_kpi', value_name='count')
        final_df.set_index("State")
        fig = px.bar(final_df, x="State", y="count", color="covid_kpi", title="Covid Figures for States", barmode='group')
        fig.update_layout(xaxis_type='category',
                          xaxis_title="Covid-19 Impacted States",
                          yaxis_title="Covid-19 Figures",
                          font_family="Courier New",
                          font_color="black",
                          title_font_family="Times New Roman",
                          title_font_color="blue",
                          legend_title_font_color="black",
                          legend_title_text='Covid Counts'
                          )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
