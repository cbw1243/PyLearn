import pandas as pd
import numpy as np
import censusdata
#import geopandas as gpd
import json
from urllib.request import urlopen
#import matplotlib.pyplot as plt
import os
import plotly.graph_objects as go
import plotly.express as px

if not os.path.exists("images"):
    os.mkdir("images")

# Read covid19 data from New York Times Github
url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
df = pd.read_csv(url)
#df.dtypes

# Download population data from census 
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.precision', 2)
countypop = censusdata.download('acs5', 2018, censusdata.censusgeo([('county', '*')]),
                                ['B01001_001E'])
countypop.columns = ['population']

# Extract fips codes
new_indices = []
#county_names = []
for index in countypop.index.tolist():
    new_index = index.geo[0][1] + index.geo[1][1]
    new_indices.append(new_index)
#    county_name = index.name.split(',')[1] 
#    county_names.append(county_name)
 
countypop['fips'] = new_indices
#countypop['county_name'] = county_names   
    
# The most recent data
df_recent = df[df.date == '2020-06-18']
df_recent = df_recent.dropna()
df_recent['fips'] = df_recent['fips'].astype(int)
df_recent['fips'] = df_recent['fips'].astype(str)
#mask = pd.to_numeric(df_recent['fips']).notnull()
#df.loc[mask] = df.loc[mask].astype(np.int64)
df_recent['fips'] = df_recent['fips'].str.zfill(5)
df_recent.dtypes
df_recent.describe()

# Merge data with the population data
df_merge = df_recent.merge(countypop, left_on = 'fips', right_on = 'fips', how = 'outer')
df_merge['deaths_percapita'] = 100*df_merge['deaths']/df_merge['population'] 
df_merge['cases_percapita'] = 100*df_merge['cases']/df_merge['population'] 
df_merge['deaths_percapita'].describe()

#hist = df_merge['deaths_percapita'].hist(bins=30)
#np.percentile( df_merge['deaths_percapita'], q = [25, 50, 60, 70, 80, 90])

# Convert to discrete values
def func(x):
    if x < 0.01:
        return "0 ~ 0.01%"
    elif x < 0.02:
        return '0.01 ~ 0.02%'
    elif x < 0.03:
        return '0.02 ~ 0.03%'
    elif x < 0.04:
        return '0.03 ~ 0.04%'
    elif x < 1:
        return '> 0.04%'
    else:
        return 'No Data' 

df_merge['level'] = df_merge['deaths_percapita'].apply(func)

# Now plot the data. 
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# =============================================================================
# fig = px.choropleth(df_merge, geojson=counties, locations='fips', color='deaths_percapita',
#                     color_continuous_scale="Viridis",
#                     range_color=(0, 0.5),
#                     scope="usa",
#                     labels={'deaths':'Deaths per capita'}
#                     )
# =============================================================================
colorscale = {'0 ~ 0.01%':"#ffffcc", '0.01 ~ 0.02%':"#c2e699", '0.02 ~ 0.03%':"#78c679", 
              '0.03 ~ 0.04%': "#31a354", '> 0.04%': "#006837", 'No Data': '#bdbdbd'}

fig = px.choropleth(df_merge, geojson=counties, locations='fips', color='level',
                    color_discrete_map=colorscale,
                    scope="usa",
                    category_orders = {'level': ['0 ~ 0.01%', '0.01 ~ 0.02%', '0.02 ~ 0.03%', '0.03 ~ 0.04%', '> 0.04%', 'No Data']},
                    labels={'level':'Deaths per capita'},
                    title = 'Figure. Total COVID-19 Deaths per Capita by County, 06/18/2020.'                   
                    )
fig.update_layout(#margin={"r":0,"t":0,"l":0,"b":0}, showlegend = True,
                  #legend=dict(x=0.5, y=1), legend_orientation="h",
                  annotations=[
       go.layout.Annotation(
            showarrow=False,
            text='Notes: Total deaths is 96,125 (equivalent to 0.029% of U.S. population).<br clear="left">Data source: The New York Times.',
            xanchor='right',
            x=1,
            # xshift=275,
            align='right',
            yanchor='bottom',
            y=-0.1,
        )])
#fig.show()

fig.write_image("images/fig1.pdf")
fig.write_image("images/fig1.png")


sum(df_merge['deaths'])/sum(df_merge['population'])
np.nansum(df_merge['deaths'])
np.nansum(df_merge['population'])
100*np.nansum(df_merge['deaths'])/np.nansum(df_merge['population'])

la_death = df_merge[df_merge.state == 'Louisiana']
np.nansum(la_death['deaths'])
np.nansum(la_death['population'])
100*np.nansum(la_death['deaths'])/np.nansum(la_death['population'])

# =============================================================================
# if not os.path.exists("images"):
#     os.mkdir("images")
# =============================================================================
