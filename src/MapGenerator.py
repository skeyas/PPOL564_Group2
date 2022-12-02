class MapGenerator:
	@staticmethod
	def create_nonwhite_population_plot_for_state(df, state):
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
	