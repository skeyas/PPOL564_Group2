import geopandas as gpd
import statsmodels.api as sm
import matplotlib.pyplot as plt

from shapely.geometry import Point, Polygon
from sklearn import linear_model


class Processor:
	@staticmethod
	def create_geocoding_columns(df):
		df['countyfips'] = df.state+df.county
		df['GEOID'] = df.state+df.county+df.tract
		return df
		
#	@staticmethod
#	def merge_and_print_data_shape(df1, df2, left_key, right_key, type_of):
			
	@staticmethod
	def prepare_data_for_regression_analysis(tri, census):
		#geocode TRI data
		geom = [Point(x) for x in tri.geocoded]
		tri = gpd.GeoDataFrame(tri, 
								  crs = {'init':'EPSG:4326'}, 
								  geometry = geom)

		#creating indicator for presence of toxic facility in tract
		census["tri_facility_in_polygon"] = census.geometry.apply(lambda x: tri.within(x).any())

		#create additional columns to include information about poverty and asthma percentage
		census['pov_percentage']=census['below_pov_line'] / census['total_pov']
		census['asthma_percentage_on1']=census['asthma_percentage']/100
		census['tri_facility_in_polygon'] = census['tri_facility_in_polygon'].astype(int)
		return census.dropna()
		
	@staticmethod
	def generate_regression(df):
		#ols 
		x = df[['non_white_percentage', 'pov_percentage', 'tri_facility_in_polygon']]
		y = df['asthma_percentage_on1']
		 
		# with sklearn
		regr = linear_model.LinearRegression()
		regr.fit(x, y)

		print('Intercept: \n', regr.intercept_)
		print('Coefficients: \n', regr.coef_)

		# with statsmodels
		# adding a constant
		x = sm.add_constant(x) 
		 
		model = sm.OLS(y, x).fit()
		 
		print_model = model.summary()
		print(print_model)
		
		#printing regression results as png

		plt.rc('figure', figsize=(6, 5))
		plt.text(0.01, 0.05, str(model.summary()), {'fontsize': 10}, fontproperties = 'monospace')
		plt.axis('off')
		plt.tight_layout()
		plt.savefig('../output/regression.png')
		
		return model