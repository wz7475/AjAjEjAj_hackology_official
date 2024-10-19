import pandas as pd
import plotly.express as px
import plotly.graph_objects
import plotly.graph_objects as go
FIG_WIDTH = 300
def create_spider_plot(df: pd.DataFrame, category: str) ->plotly.graph_objects.Figure:
	filtered_data = df[df['category'] == category]
	fig = go.Figure()
	fig.add_trace(go.Scatterpolar(
		r=filtered_data['value'],
		theta=filtered_data['subcategory'],
		fill='toself',
		name=category
	))
	fig.update_layout(
		# template='plotly_dark',
		polar=dict(
			radialaxis=dict(
				visible=True,
				range=[0, max(filtered_data['value'])]  # Adjust this based on your data
			)),
		showlegend=False,
		# title=dict(
		# 	text=f"{category.capitalize()}",
		# 	x=0.5,  # Center the title
		# 	xanchor='center',
		# 	yanchor='top',
		# 	font=dict(size=20)  # Adjust the font size as needed
		# ),
		paper_bgcolor='rgba(0,0,0,0)',  # Transparent background for the overall figure
		plot_bgcolor='rgba(0,0,0,0)',   # Transparent background for the plot area
		margin=dict(l=70, r=70, t=40, b=40),
		width=FIG_WIDTH,
		height=FIG_WIDTH,
	)
	return fig

import plotly.graph_objects as go
import pandas as pd

def create_bar_plot(df: pd.DataFrame, category: str) -> go.Figure:
	# Filter data based on the selected category
	filtered_data = df[df['category'] == category]

	# Create the figure
	fig = go.Figure()

	# Add bar trace
	fig.add_trace(go.Bar(
		x=filtered_data['subcategory'],   # x-axis categories
		y=filtered_data['value'],         # y-axis values
		name=category,
		marker=dict(
			color='lightblue',            # Customize color as needed
			line=dict(color='black', width=1)  # Outline the bars with black
		)
	))

	fig.update_layout(
# 		template='plotly_dark',

		showlegend=False,                  # Disable legend
		paper_bgcolor='rgba(0,0,0,0)',     # Transparent background for the overall figure
		plot_bgcolor='rgba(0,0,0,0)',      # Transparent background for the plot area
		margin=dict(l=70, r=70, t=40, b=40),
		width=FIG_WIDTH,
		height=FIG_WIDTH,
		# Uncomment the following lines if title is needed
		# title=dict(
		#     text=f"{category.capitalize()}",
		#     x=0.5,  # Center the title
		#     xanchor='center',
		#     yanchor='top',
		#     font=dict(size=20)  # Adjust the font size as needed
		# ),
	)

	return fig
