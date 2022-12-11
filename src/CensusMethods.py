import pandas as pd
import geopandas as gpd
import numpy as np

import requests

from us import states
from census import Census

class CensusMethods:
	def __init__(self, api_key):
		self.c = Census(api_key)
		self.states_fips = states.mapping('abbr', 'fips')
		self.non_contiguous_us = ["MP", "PR", "GU", "AS", "AK", "VI", "HI"]

	
	def retrieve_all_variables(self):
		# List of all variables: https://api.census.gov/data/2019/acs/acs5/variables.html
		all_tables = pd.DataFrame(self.c.acs5.tables())
		all_vars = [pd.DataFrame(requests.get(one_table).json()['variables']).T
						for one_table in all_tables.variables]
		self.all_vars_df = pd.concat(all_vars)
		self.all_vars_df['varname'] = self.all_vars_df.index
		
	def retrieve_subset_of_variables(self, vars_to_retrieve):
		return self.all_vars_df.loc[vars_to_retrieve]
		
	
	#retrieve data according to year and state abbreviation
	def retrieve_census_data_by_state_and_year(self, fields, state, county, tract, year):
		return self.c.acs5.state_county_tract(fields = fields,
										  state_fips = eval(f"states.{state}.fips"),
										  county_fips = county,
										  tract = tract,
										  year = year)
	
	#retrieve data for list of states
	def retrieve_census_data_for_list_of_states_by_year(self, fields, states, county, tract, year):
		return {state: self.retrieve_census_data_by_state_and_year(fields, state, county, tract, year) for state in states}
		
	
	def recode_column_names_for_retrieved_data(self, df, relevant_values):
		census = pd.concat([pd.DataFrame(df[state]) for state in df])
		d0 = relevant_values['label2']
		d = d0.to_dict()
		d.update({'state':'state','county':'county','tract':'tract'})
		return census.rename(columns=d)										  
	
	def create_geocoded_state_df_with_demographics_data(self, state, df):
		try:
			#retrieve shapefile for state
			tract = gpd.read_file(f"https://www2.census.gov/geo/tiger/TIGER2019/TRACT/tl_2019_{self.states_fips[state]}_tract.zip")
			tract = tract.to_crs(epsg = 4326)
			
			#generate GEOID from fields
			df["GEOID"] = df["state"] + df["county"] + df["tract"]
			
			#computer non-white percentage
			df['non_white_percentage'] = 1 - (df.B03002_003E / df.B01003_001E)
			
			print(f"Shape of tract level shapefile df: {tract.shape}")
			print(f"Shape of state census data df: {df.shape}")
						
			merged = tract.merge(df, on = "GEOID")
			
			print(f"Shape of merged df: {merged.shape}")
						
			return merged
		except:
			print("Invalid state")
			
	def retrieve_census_tract_shapefile_for_state(self, state):	
		#retrieve shapefile for state
		q = f'https://www2.census.gov/geo/tiger/TIGER2019/TRACT/tl_2019_{self.states_fips[state]}_tract.zip'
		return gpd.read_file(q)  
		
	def retrieve_census_tract_shapefile_for_state_list(self, states):
		#retrieve shapefile for each state in list; skip if the state fips code does not exist
		dfs = []
		for s in states:
			try:
				dfs.append(self.retrieve_census_tract_shapefile_for_state(s))
			except:
				continue
		return pd.concat(dfs)
	
	def create_population_columns(self, census):
		census['white_percentage']=census.white / census.total_pop
		census['non_white_percentage']= 1-(census.white / census.total_pop)
		return census

	#remove states not in contiguous US
	def create_contiguous_us_df_with_tract_level_shapefiles(self, census, tract):
		print(census.shape)
		print(tract.shape)
		
		us_merge = pd.merge(tract, census, on = "GEOID")
		print(us_merge.shape)
		us_merge["STATE"] = us_merge["STATEFP"].apply(lambda x: list(self.states_fips.keys())[list(self.states_fips.values()).index(x)])
		return us_merge[~us_merge["STATE"].isin(self.non_contiguous_us)]
	
	def create_county_level_subset(self, df):
		#dissolve to county level
		df = df.dissolve(by = ["STATEFP", "COUNTYFP"], aggfunc = "sum")
		
		#create percentage columns for white and nonwhite
		df['white_percentage']=df['white'] / df['total_pop']
		df['non_white_percentage']= 1-(df['white'] / df['total_pop'])
		return df.reset_index()

	def create_county_level_asthma_subset(self, df):
		#create county level dataframe
		df = df.dissolve(by = ["STATEFP", "COUNTYFP"], aggfunc = "sum")
		
		#create percentage columns
		df['white_percentage']=df['white'] / df['total_pop']
		df['non_white_percentage']= 1-(df['white'] / df['total_pop'])
		df['asthma_percentage']=df['asthma_cases'] / df['total_pop']
		
		conditions_nw = [
			(df['white_percentage'] >= 0.7),
			(df['white_percentage'] < 0.7),
		]

		values_nw = [df.asthma_percentage, 0]
		values_w = [0, df.asthma_percentage]

		#Create column of asthma rates for counties above or below 70% white
		df['asthma_non_white'] = np.select(conditions_nw, values_w)
		df['asthma_white'] = np.select(conditions_nw, values_nw)
		return df.reset_index()

	
	
	
	