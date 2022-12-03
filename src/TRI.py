import re

import pandas as pd

class TRI:
	@staticmethod
	def clean_column_names(df):
		df.columns=df.columns.str.replace(r'\d|-|\.','').str.strip()
		return df
	
	@staticmethod
	def return_records_present_in_both_sets(df1, df2):
		return df2[TRI.clean_column_names(df2)["TRIFD"].isin(TRI.clean_column_names(df1)["TRIFD"])]
		
	@staticmethod
	def subset_and_geocode(df):
		non_contiguous_us = ["MP", "PR", "GU", "AS", "AK", "VI", "HI"]
		df = df[~df["ST"].isin(non_contiguous_us)]
		df = df[(df['STACK AIR'] > 0) | df["FUGITIVE AIR"] > 0]

		df = df[(df['STACK AIR'] > df['STACK AIR'].quantile(0.90)) | (df["FUGITIVE AIR"] > df['FUGITIVE AIR'].quantile(0.90))]
		df["geocoded"] = [(df.iloc[a]['LONGITUDE'], df.iloc[a]['LATITUDE']) 
							  for a in range(len(df))]
		return df
	
	@staticmethod
	def subset_to_state(df, state):
		return df[df["ST"] == state]