import pandas as pd
import geopandas as gpd
import requests

from us import states
from census import Census

class CensusMethods:
	def __init__(self, api_key):
		self.c = Census(api_key)
		self.states_fips = states.mapping('abbr', 'fips')
	
	def retrieve_all_variables(self):
		# List of all variables: https://api.census.gov/data/2019/acs/acs5/variables.html
		all_tables = pd.DataFrame(self.c.acs5.tables())
		all_vars = [pd.DataFrame(requests.get(one_table).json()['variables']).T
						for one_table in all_tables.variables]
		self.all_vars_df = pd.concat(all_vars)
		self.all_vars_df['varname'] = self.all_vars_df.index
		
	def retrieve_subset_of_variables(self, vars_to_retrieve):
		return self.all_vars_df.loc[vars_to_retrieve]
		
	
		
	def retrieve_census_data_by_state_and_year(self, fields, state, county, tract, year):
		return self.c.acs5.state_county_tract(fields = fields,
										  state_fips = eval(f"states.{state}.fips"),
										  county_fips = county,
										  tract = tract,
										  year = year)
	
	def retrieve_census_data_for_list_of_states_by_year(self, fields, states, county, tract, year):
		return {state: self.retrieve_census_data_by_state_and_year(fields, state, county, tract, year) for state in states}
										  
	def create_geocoded_state_df_with_demographics_data(self, state, df):
		try:
			tract = gpd.read_file(f"https://www2.census.gov/geo/tiger/TIGER2019/TRACT/tl_2019_{self.states_fips[state]}_tract.zip")
			tract = tract.to_crs(epsg = 4326)
			df["GEOID"] = df["state"] + df["county"] + df["tract"]
			df['non_white_percentage'] = 1 - (df.B03002_003E / df.B01003_001E)
			return tract.merge(df, on = "GEOID")
		except:
			print("Invalid state")
			
	def retrieve_census_tract_shapefile_for_state(self, state):		
		q = f'https://www2.census.gov/geo/tiger/TIGER2019/TRACT/tl_2019_{self.state_fips[state]}_tract.zip'
		return gpd.read_file(q)  
		
	def retrieve_census_tract_shapefile_for_state_list(states):
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
	
	
	
	
	
	
	
	
	
	
	
	
	
	