# IMPORTING the libraries
import numpy as nu 
import pandas as pa 
import matplotlib.pyplot as py
from mpl_toolkits.basemap import Basemap
import seaborn as sns
import os 
%matplotlib inline
print(os.listdir("../input"))

#Getting the input and stored as data frame
file_name = "../input/"../input/temperaturein/temp.csv""
df = pa.read_csv(file_name, na_values=[-9999])
df.fillna(0, inplace=True)   
df.shape

co2 = pa.read_csv("../input/output/output_temp.csv",skiprows = 3)
co2.head()

def get_temp(year, month):
    temp_df = df.ix[df.year==year]
    temp_df = temp_df.ix[temp_df.month==month]
    return nu.array(temp_df.iloc[:,3:]) / 100.

lons = nu.array([-180, -175, -170, -165, -160, -155, -150, -145, -140, -135, -130, -125, -120, -115, -110, -105, -100, -95, -90, -85, -80, -75, -70, -65, -60, -55, -50, -45, -40, -35, -30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180])
lats = nu.array([90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 25, 20, 15, 10, 5, 0, -5, -10, -15, -20, -25, -30, -35, -40, -45, -50, -55, -60, -65, -70, -75, -80, -85, -90])
lons, lats = nu.meshgrid(lons, lats)

# Temperature of 1994
temperature = get_temp(1994, 1)
temperature[temperature<-4] = -4
temperature[temperature>4] = 4

fig = py.figure(figsize=(12,8))
ax = fig.add_axes([0.05,0.05,0.9,0.9])
#creating a basic map
m = Basemap(projection='gall',
              llcrnrlon = -180,             
              llcrnrlat = -90,              
              urcrnrlon = 180,              
              urcrnrlat = 90,               
              resolution = 'l',
              area_thresh = 1000000.0
              )
m.drawcoastlines()
m.drawcountries()

# polting the ice with color
im = m.pcolormesh(lons,lats,temperature,shading='flat',cmap=py.cm.seismic,latlon=True)
# adding color bar
cb = m.colorbar(im,"bottom", size="5%", pad="5%")
# adding a title
ax.set_title('Temperature in 1994')
py.show()

import matplotlib.animation as animation

years = range(1990, 2017, 1)
# getting the temp for year 1980
temperature = get_temp(1990, 7)
temperature[temperature<-5] = -5
temperature[temperature>5] = 5
fig = py.figure(figsize=(12,8))
ax = fig.add_axes([0.05,0.05,0.9,0.9])

m = Basemap(projection='gall',
              llcrnrlon = -180,              
              llcrnrlat = -60,               
              urcrnrlon = 180,               
              urcrnrlat = 90,               
              resolution = 'l',
              area_thresh = 1000000.0
              )
m.drawcoastlines()
m.drawcountries()

# plotting ice with the color
im = m.pcolormesh(lons,lats,temperature,shading='flat',cmap=py.cm.seismic,latlon=True)

# adding color bar
cb = m.colorbar(im,"bottom", size="5%", pad="5%")

# adding a title 
ax.set_title('Temperature in July 1880')
ax.set_xlabel("Temperature differences in (ºC)")


def updating_figure(ind):
    year = years[ind]
    temperature = get_temp(year, 7)
    temperature[temperature<-5] = -5
    temperature[temperature>5] = 5
    m.pcolormesh(lons,lats,temperature,shading='flat',cmap=py.cm.seismic,latlon=True)
    ax.set_title('Temperature in July '+str(year))
    ax.set_xlabel("Temperature differences in (ºC)")
    return im,

ai = animation.FuncAnimation(fig, updating_figure, frames=len(years))
ai.save('lb.gif', fps=0.33, writer='imagemagick')