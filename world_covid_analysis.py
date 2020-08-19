import pandas as pd     #(version 1.0.0)
import plotly           #(version 4.5.4) pip install plotly==4.5.4
import plotly.express as px

import dash             #(version 1.9.1) pip install dash==1.9.1
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
server = app.server
#---------------------------------------------------------------
#Taken from https://www.ecdc.europa.eu/en/geographical-distribution-2019-ncov-cases
df = pd.read_excel("COVID-19-geographic-disbtribution-worldwide.xlsx")

dff = df.groupby(['continentExp','countriesAndTerritories'], as_index=False)[['deaths','cases']].sum()
print (dff[:5])
data_columns = ['Continent', 'CountriesOrTerritories', 'Total Deaths', 'Total Cases']
dff_columns = ['continentExp', 'countriesAndTerritories', 'deaths', 'cases']
#---------------------------------------------------------------
app.layout = html.Div([
html.H1("World Covid Analysis using Dash & Plotly Visualizations", style={'text-align': 'center'}),
    html.Div([
        dash_table.DataTable(
            id='datatable_id',
            data=dff.to_dict('records'),
            columns=[{
                'name': col,
                'id': dff_columns[idx]
            } for (idx, col) in enumerate(data_columns)],
            editable=False,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            row_selectable="multi",
            row_deletable=False,
            selected_rows=[],
            page_action="native",
            page_current= 0,
            page_size= 10,
            # page_action='none',
            # style_cell={
            # 'whiteSpace': 'normal'
            # },
            # fixed_rows={ 'headers': True, 'data': 0 },
            # virtualization=False,
            style_cell_conditional=[
                {'if': {'column_id': 'continentExp'},
                 'width': '20%', 'textAlign': 'center'},
                {'if': {'column_id': 'countriesAndTerritories'},
                 'width': '40%', 'textAlign': 'center'},
                {'if': {'column_id': 'deaths'},
                 'width': '20%', 'textAlign': 'center'},
                {'if': {'column_id': 'cases'},
                 'width': '20%', 'textAlign': 'center'},

            ],
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            }
        ),
    ],className='row'),

    html.Div([
        html.Div([
            dcc.Dropdown(id='linedropdown',
                options=[
                         {'label': 'Deaths', 'value': 'deaths'},
                         {'label': 'Cases', 'value': 'cases'}
                ],
                value='deaths',
                multi=False,
                clearable=False
            ),
        ],className='six columns'),

        html.Div([
        dcc.Dropdown(id='piedropdown',
            options=[
                     {'label': 'Deaths', 'value': 'deaths'},
                     {'label': 'Cases', 'value': 'cases'}
            ],
            value='cases',
            multi=False,
            clearable=False
        ),
        ],className='six columns'),

    ],className='row'),

    html.Div([
        html.Div([
            dcc.Graph(id='linechart'),
        ],className='six columns'),

        html.Div([
            dcc.Graph(id='piechart'),
        ],className='six columns'),

    ],className='row'),


])

#------------------------------------------------------------------
@app.callback(
    [Output('piechart', 'figure'),
     Output('linechart', 'figure')],
    [Input('datatable_id', 'selected_rows'),
     Input('piedropdown', 'value'),
     Input('linedropdown', 'value')]
)
def update_data(chosen_rows,piedropval,linedropval):
    if len(chosen_rows)==0:
        df_filterd = dff[dff['countriesAndTerritories'].isin(['India','United_States_of_America','Brazil','Russia'])]
    else:
        print(chosen_rows)
        df_filterd = dff[dff.index.isin(chosen_rows)]

    pie_chart=px.pie(
            data_frame=df_filterd,
            names='countriesAndTerritories',
            values=piedropval,
            hole=.3,
            labels={'countriesAndTerritories':'Countries'}
            )


    #extract list of chosen countries
    list_chosen_countries=df_filterd['countriesAndTerritories'].tolist()
    #filter original df according to chosen countries
    #because original df has all the complete dates
    df_line = df[df['countriesAndTerritories'].isin(list_chosen_countries)]

    line_chart = px.line(
            data_frame=df_line,
            x='dateRep',
            y=linedropval,
            color='countriesAndTerritories',
            labels={'countriesAndTerritories':'Countries', 'dateRep':'date'},
            )
    line_chart.update_layout(uirevision='foo')

    return (pie_chart,line_chart)

#------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)