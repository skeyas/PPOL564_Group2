class Processor:
	@staticmethod
	def create_geocoding_columns(df):
		df['countyfips'] = df.state+df.county
		df['GEOID'] = df.state+df.county+df.tract
		return df
		
	