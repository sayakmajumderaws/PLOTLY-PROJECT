import pandas as pd
import datetime
import plotly.express as px
import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
df = pd.read_csv("https://api.covid19india.org/csv/latest/districts.csv")
state_options = df['State'].unique()
app.layout = html.Div([

    html.H2("Covid District Level Analysis with Scatter Plot", style={'text-align': 'center'}),

        html.Div([
            html.Label(['Select Time Frame:'],style={'font-weight': 'bold'}),
            dcc.RadioItems(
                id='xaxis_raditem',
                options=[
                         {'label': 'Last 7 days', 'value': '7day'},
                         {'label': 'Last 15 days', 'value': '15day'},
                         {'label': 'Last 30 days', 'value': '30day'}
                ],
                value='7day',
                style={"width": "50%"}
            ),
        ]),
        html.Div([
            html.Label(['Select State:'], style={'font-weight': 'bold'}),
            dcc.Dropdown(id="select_state",
                         options=[{'label': i, 'value': i} for i in state_options],
                         multi=False,
                         style={'width': "40%"},
                         placeholder="Select a State",
                         )]),
        html.Div([
            dcc.Graph(id='the_graph')
        ]),

])
@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='xaxis_raditem', component_property='value'),
     Input(component_id='select_state', component_property='value')]
)
def update_graph(x_axis,select_state):
    if select_state is None:
        fig = {}
    else:
        df_temp = df[df['State'] == select_state]
        df_temp['Date'] = pd.to_datetime(df_temp['Date'], format="%Y-%m-%d")
        finaldf = df_temp[df_temp.Date > datetime.datetime.now() - pd.to_timedelta(str(x_axis))]

        finaldf['DateVal'] = pd.to_datetime(finaldf['Date'], format='%Y-%m-%d', errors='coerce').dt.strftime("%d-%b")
        finaldf.sort_values('Date', ascending=True)
        fig = px.scatter(finaldf, x="District", y=["Confirmed", "Recovered", "Deceased"], animation_frame="DateVal",

                         title="Covid Progress across Districts ",
                         # customize label
                         labels={
                             "DateVal": "TimeLine"
                         }
                         )
        fig.update_layout(
            xaxis_title='',
            yaxis_title="Covid-19 Impact",
            font_family="Courier New",
            font_color="black",
            title_font_family="Times New Roman",
            title_font_color="blue",
            legend_title_font_color="black",
            legend_title_text='Cumulative Count'
        )

        fig.update_layout(title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 20}}

                          )
        fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 800
        fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 800
        fig.data[0].name = 'Confirmed'
        fig.data[1].name = 'Recovered'
        fig.data[2].name = 'Deceased'
        fig.data[0]['marker'].update(size=14)
        fig.data[1]['marker'].update(size=14)
        fig.data[2]['marker'].update(size=14)
        fig.data[0]['marker'].update(color='#22bc22')
        fig.data[1]['marker'].update(color="#fda026")
        fig.data[2]['marker'].update(color="#00FFFF")

        for x in fig.frames:
            x.data[0]['marker']['color'] = '#22bc22'
            x.data[1]['marker']['color'] = '#fda026'
            x.data[2]['marker']['color'] = '#00FFFF'

    return fig
if __name__ == '__main__':
    app.run_server(debug=True)