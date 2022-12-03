import json

import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

from us import states
from urllib.request import urlopen


class MapGenerator:
	@staticmethod
	def create_nonwhite_population_plot_for_state_tract(df, state):
		# Create subplots
		fig, ax = plt.subplots(1, 1, figsize = (20, 10))

		# Plot data
		df.plot(column = "non_white_percentage",
							   ax = ax,
							   cmap = "RdPu",
							   legend = True)

		# Stylize plots
		plt.style.use('bmh')

		# Set title
		ax.set_title(f'Non-white population (%) in {eval(f"states.{state}.name")}', fontdict = {'fontsize': '25', 'fontweight' : '3'})
		
		
	@staticmethod
	def create_nonwhite_population_plot_for_state_county(df, state):
		df = df[['geometry','non_white_percentage']]
		# Create subplots
		fig, ax = plt.subplots(1, 1, figsize = (20, 10))

		# Plot data
		df.plot(column = "non_white_percentage",
							   ax = ax,
							   cmap = "RdPu",
							   legend = True)

		# Stylize plots
		plt.style.use('bmh')

		# Set title
		ax.set_title(f'Non-white population (%) in {eval(f"states.{state}.name")}, counties', fontdict = {'fontsize': '25', 'fontweight' : '3'})
		
	@staticmethod
	def create_us_level_population_plot_county(census):
		with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
			counties = json.load(response)
		census_analysis = census[['state','county','tract','countyfips','GEOID','white_percentage','non_white_percentage']]
		census_analysis_county = census[['state','county','tract','countyfips','GEOID','white','total_pop']]
		
		census_county = census_analysis_county.groupby('countyfips').sum().reset_index()
		census_county['white_percentage']=census_county.white / census_county.total_pop
		census_county['non_white_percentage']= 1-(census_county.white / census_county.total_pop)

		fig_us_county_pop = px.choropleth(census_county, geojson=counties, locations='countyfips', color='non_white_percentage',
								   color_continuous_scale="Viridis",
								   range_color=(0, 1),
								   scope="usa",
								   labels={'non_white_percentage':'% of non-white population'}
								  )
		fig_us_county_pop.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
		
		return fig_us_county_pop
		
	@staticmethod
	def create_us_population_plot_tract(census_with_shapefiles):
		# Create subplots
		fig, ax = plt.subplots(1, 1, figsize = (20, 10))

		# Plot data
		census_with_shapefiles.plot(column = "non_white_percentage",
							   ax = ax,
							   cmap = "RdPu",
							   legend = True)

		# Stylize plots
		plt.style.use('bmh')

		# Set title
		ax.set_title('Non-white population (%) in the United States', fontdict = {'fontsize': '25', 'fontweight' : '3'})
	