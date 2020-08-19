import pandas as pd
import plotly.express as px
import json
df = pd.read_csv('https://api.covid19india.org/csv/latest/statewise_tested_numbers_data.csv')
group_df = df.groupby('State').agg({'Total Tested': 'max','Positive':'max'}).reset_index()
group_df['Test Positivity Rate'] = round((group_df['Positive']/group_df['Total Tested'])*100,2)
group_df.set_index("State", inplace=True, drop=True)
group_df.loc['Jammu and Kashmir'] += group_df.loc['Ladakh']
group_df.drop(['Ladakh'], inplace=True)
group_df.reset_index(inplace=True)
india_states = json.load(open("C:\\Projects\\Maxis\\states_india.geojson", "r"))
state_id_map = {}
for feature in india_states["features"]:
    feature["id"] = feature["properties"]["state_code"]
    state_id_map[feature["properties"]["st_nm"]] = feature["id"]
group_df["id"] = group_df["State"].apply(lambda x: state_id_map[x])
fig = px.choropleth(
    group_df,
    locations="id",
    geojson=india_states,
    color_continuous_scale=px.colors.sequential.Cividis_r,
    range_color=(0, 12),
    color="Test Positivity Rate",
    hover_name="State",
    hover_data=["Total Tested","Positive",'Test Positivity Rate'],
    title="India Covid-19 Testing and Positivity Rate using Choropleth Maps"

)
fig.update_geos(fitbounds="locations", visible=False)
print(fig.show())