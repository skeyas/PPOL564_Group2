import pandas as pd

class CDC:
	@staticmethod
	def subset_CDC_data_to_year_and_type(df, year, condition_type):
		df = df[(df.Year == year) & (df.Short_Question_Text == condition_type)]

		#subset to relevant columns
		df = df[['StateAbbr','CountyName','CountyFIPS',
													'LocationName','Measure','Data_Value',
													 'Data_Value_Unit','TotalPopulation',
													 'Geolocation','LocationID']].copy()
		#Calculate absolute value of population with asthma
		df['value_numeric'] = df.Data_Value.astype(float) *\
									df.TotalPopulation.astype(float) *0.01
									
		return df
		
	@staticmethod
	def format_location_ids_for_merging(df):
		#convert to same datatype, pad for merging
		df['LocationID'] = df.LocationID.astype(str)
		df['GEOID'] = df.LocationID.str.pad(width = 11,
                                                     side = "left",
                                                     fillchar = "0")
		return df