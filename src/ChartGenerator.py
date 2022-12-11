import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm

from matplotlib.pyplot import figure


class ChartGenerator:
	@staticmethod
	def plot_linearity(df):
		plt.scatter(df['non_white_percentage'], df['asthma_percentage_on1'], color='red')
		plt.title('Exploring Linearity - % Asthma cases Vs % Non-white population', fontsize=11)
		plt.xlabel('% Non-white population', fontsize=10)
		plt.ylabel('% Asthma cases', fontsize=10)
		plt.grid(True)
		plt.show()

		plt.scatter(df['pov_percentage'], df['asthma_percentage_on1'], color='blue')
		plt.title('Exploring Linearity - % Asthma cases Vs % Population below poverty line', fontsize=11)
		plt.xlabel('% Population below poverty', fontsize=10)
		plt.ylabel('% Asthma cases', fontsize=10)
		plt.grid(True)
		plt.show()
		
	@staticmethod
	def plot_partial_regression(model):
		fig, ax = plt.subplots(figsize=(8, 8))
		figure = sm.graphics.plot_partregress_grid(model, fig=fig)
		figure.savefig("../output/regression_graph.png")