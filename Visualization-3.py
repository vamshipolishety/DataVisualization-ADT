import numpy as npy
import pandas as pds
import matplotlib.pyplot as plt
%matplotlib inline
import plotly.offline as pyoff
pyoff.init_notebook_mode(connected=True)
import plotly.graph_objs as gobj
import plotly.tools as tol
import seaborn as sbn
import time
import warnings
warnings.filterwarnings('ignore')

#now first we will take csv file for global temperature according to country
country_temp = pds.read_csv('../input/WorldTemperaturesByCountry.csv')		

#now we will map the countries and remove duplication

country_temp_noduplication = country_temp[~country_temp['Country'].isin(
    ['Denmark', 'Antarctica', 'France', 'Europe', 'Netherlands',
     'United Kingdom', 'Africa', 'South America'])]

country_temp_noduplication = country_temp_noduplication.replace(
   ['Denmark (Europe)', 'France (Europe)', 'Netherlands (Europe)', 'United Kingdom (Europe)'],
   ['Denmark', 'France', 'Netherlands', 'United Kingdom'])
   
#Let's take average temperature for each country

allcountry = npy.unique(country_temp_noduplication['Country'])
mean_temperature = []
for country in allcountry:
    mean_temperature.append(country_temp_noduplication[country_temp_noduplication['Country'] == 
                                               country]['AverageTemperature'].mean())
											   
			data = [ dict(
        type = 'choropleth',
        locations = allcountry,
        z = mean_temperature,
        locationmode = 'country names',
        text = allcountry,
        marker = dict(
            line = dict(color = 'rgb(0,0,0)', width = 1)),
            colorbar = dict(autotick = True, tickprefix = '', 
            title = '# Average\nTemperature,\n°C')
            )
       ]
	   
	   layout = dict(
    title = 'All countries with thier average land temperature',
    geo = dict(
        showframe = False,
        showocean = True,
        oceancolor = 'rgb(0,255,255)',
        projection = dict(
        type = 'orthographic',
            rotation = dict(
                    lon = 60,
                    lat = 10),
        ),
        lonaxis =  dict(
                showgrid = True,
                gridcolor = 'rgb(102, 102, 102)'
            ),
        lataxis = dict(
                showgrid = True,
                gridcolor = 'rgb(102, 102, 102)'
                )
            ),
        )
		
		fig = dict(data=data, layout=layout)
pyoff.iplot(fig, validate=False, filename='worldmap')


#Now we will Sort the countries by their average temperature and display the data in a Horizontal Bar format 

mean_temp_bar, countries_bar = (list(x) for x in zip(*sorted(zip(mean_temperature, allcountry), 
                                                             reverse = True)))
sbn.set(font_scale=0.8) 
f, ax = plt.subplots(figsize=(4, 50))
colors_cw = sbn.color_palette('coolwarm', len(allcountry))
sbn.barplot(mean_temp_bar, countries_bar, palette = colors_cw[::-1])
Text = ax.set(xlabel='Avg temp', title='all country avg temp')

#Is there a global warming?

#So now lets see the effect of global warming by reading data from "GlobalTemperatures.csv" file.

g_temperature = pds.read_csv("../input/WorldTemperatures.csv")

#Extract the year from a date
years = npy.unique(g_temperature['dt'].apply(lambda x: x[:4]))
temp_global = []
temp_global_uncertain = []

for year in years:
    temp_global.append(g_temperature[g_temperature['dt'].apply(
        lambda x: x[:4]) == year]['LandAverageTemperature'].mean())
    temp_global_uncertain.append(g_temperature[g_temperature['dt'].apply(
                lambda x: x[:4]) == year]['LandAverageTemperatureUncertainty'].mean())
				
				trace0 = gobj.Scatter(
    x = years, 
    y = npy.array(temp_global) + npy.array(temp_global_uncertain),
    fill= None,
    mode='lines',
    name='Uncertainty top',
    line=dict(
        color='rgb(0, 255, 255)',
    )
)

trace1 = gobj.Scatter(
    x = years, 
    y = npy.array(temp_global) - npy.array(temp_global_uncertain),
    fill='tonexty',
    mode='lines',
    name='Uncertainty bot',
    line=dict(
        color='rgb(0, 255, 255)',
    )
)

trace2 = gobj.Scatter(
    x = years, 
    y = temp_global,
    name='Average Temperature',
    line=dict(
        color='rgb(199, 121, 093)',
    )
)

data = [trace0, trace1, trace2]

layout = gobj.Layout(
    xaxis=dict(title='Year'),
    yaxis=dict(title='Temperature Avg'),
    title='world Avg Temp',
    showlegend = False)

fig = gobj.Figure(data=data, layout=layout)
pyoff.iplot(fig)