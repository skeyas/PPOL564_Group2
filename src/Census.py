import pandas as pd
import geopandas as gpd

from us import states
from census import Census

class Census:
	def __init__(api_key):
		self.c = Census(api_key)
		self.states_fips = = states.mapping('abbr', 'fips')
	
	def retrieve_all_variables():
		# List of all variables: https://api.census.gov/data/2019/acs/acs5/variables.html
		all_tables = pd.DataFrame(self.c.acs5.tables())
		all_vars = [pd.DataFrame(requests.get(one_table).json()['variables']).T
						for one_table in all_tables.variables]
		self.all_vars_df = pd.concat(all_vars)
		self.all_vars_df['varname'] = all_vars_df.index
		return self.all_vars_df
		
	def retrieve_subset_of_variables(vars_to_retrieve):
		return self.all_vars_df.loc[vars_to_retrieve]
		
	
		
	def retrieve_race_data_by_state_and_year(fields, state, county, tract, year):
		return self.c.acs5.state_county_tract(fields = fields,
										  state_fips = eval(f"states.{state}.fips"),
										  county_fips = county,
										  tract = tract,
										  year = year)
										  
	def create_geocoded_state_df_with_demographics_data(state, df):
		try:
			tract = gpd.read_file(f"https://www2.census.gov/geo/tiger/TIGER2019/TRACT/tl_2019_{states_fips[state]}_tract.zip")
			tract = tract.to_crs(epsg = 4326)
			df["GEOID"] = df["state"] + df["county"] + df["tract"]
			df['non_white_percentage'] = 1 - (df.B03002_003E / df.B01003_001E)
			return tract.merge(df, on = "GEOID")
		except:
			print("Invalid state")
			
	def retrieve_census_tract_shapefile_for_state(state):		
		q = f'https://www2.census.gov/geo/tiger/TIGER2019/TRACT/tl_2019_{self.state_fips[state]}_tract.zip'
		return gpd.read_file(q)  
		
	def retrieve_census_tract_shapefile_for_state_list(states):
		dfs = []
		for s in states:
			try:
				dfs.append(retrieve_census_tract_shapefile_for_state(s))
			except:
				continue
		return pd.concat(dfs)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	