import pandas as pd     #(version 1.0.0)
import plotly           #(version 4.5.0)
import plotly.express as px

import dash             #(version 1.8.0)
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
server = app.server
df = pd.read_csv(r"https://api.covid19india.org/csv/latest/case_time_series.csv")
df['Date']= df['Date'] + " 20"
df['DateVal'] = pd.to_datetime(df['Date'].str.strip(), format='%d %B %y', errors='coerce').dt.strftime("%Y-%m-%d")
df['Month'] = pd.to_datetime(df['DateVal']).dt.strftime("%b-%Y")

app.layout = html.Div([

    html.H1("Covid India Cumulative Case Count Analysis with Line Chart having Time Filter", style={'text-align': 'center'}),
    dcc.Checklist(id="select_count",
                  options=[
                      {"label": "Confirmed", "value": "Total Confirmed"},
                      {"label": "Recovered", "value": "Total Recovered"},
                      {"label": "Deceased", "value": "Total Deceased"}
                      ],
                  value=["Total Confirmed","Total Recovered","Total Deceased"],
                  style={"display":"block"}

                  ),
    html.Br(),
    html.Br(),
    html.Div([
        dcc.Graph(id='count_graph', figure={})
    ])
])
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    Output(component_id='count_graph', component_property='figure'),
   [Input(component_id='select_count', component_property='value')]
)
def build_graph(select_count):
    fig = px.line(df, x="DateVal", y=select_count,
                  labels={
                      "Total Confirmed": "Total Confirmed Cases",
                      "Total Recovered": "Total Number of Recovered Patients",
                      "Total Deceased": "Total Number of Deceased Patients"
                  },
                  title="Overall COVID-19 Cases Recoveries and Deaths in India"
                  )
    # Add range slider
    fig.update_xaxes(rangeslider_visible=True,
                     rangeselector=dict(
                         buttons=list([
                             dict(count=1, label="1m", step="month", stepmode="backward"),
                             dict(count=6, label="6m", step="month", stepmode="backward"),
                             dict(count=1, label="1y", step="year", stepmode="backward"),
                             dict(step="all")
                         ])
                     )
                     )
    fig.update_layout(
        xaxis_title="Covid-19 Timeline",
        yaxis_title="Covid-19 Impact",
        font_family="Courier New",
        font_color="black",
        title_font_family="Times New Roman",
        title_font_color="blue",
        legend_title_font_color="black",
        legend_title_text='Cumulative Count'

    )

    return fig

#---------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=False)
