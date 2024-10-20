import pandas as pd
import plotly.express as px
import plotly.graph_objects
import plotly.graph_objects as go
FIG_WIDTH = 350

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
		title=dict(
			text=f"{category.upper()}",
			x=0.5,  # Center the title
			xanchor='center',
			yanchor='top',
			font=dict(size=20)  # Adjust the font size as needed
		),
		paper_bgcolor='rgba(0,0,0,0)',  # Transparent background for the overall figure
		plot_bgcolor='rgba(0,0,0,0)',   # Transparent background for the plot area
		margin=dict(l=80, r=80, t=50, b=50),
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
		),

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
		title=dict(
		    text=f"{category.capitalize()}",
		    x=0.5,  # Center the title
		    xanchor='center',
		    yanchor='top',
		    font=dict(size=20)  # Adjust the font size as needed
		),
	)

	return fig

def geo_plot(y_path: str):
	df_1=pd.read_csv("../data/merged_data.csv", index_col=0)[['lon', 'lat']]
	df_2=pd.read_csv(f"../data/{y_path}", index_col=0)
	df_geo=df_2.join(df_1, how='right').rename({'0':'y'}, axis=1)
	limits = [(0,500),(500,1000),(1000,1500),(1500,2000),(2000,300000)]
	colors = ["royalblue","lightseagreen", "orange", "crimson", "lightgrey"]
	scale = 100

	fig = go.Figure(go.Choropleth(
		locations=['POL'],
		z=[1],
		locationmode='ISO-3',
		colorscale='Greys',
		showscale=False
	))

	for i, lim in enumerate(limits):
		df_sub = df_geo[lim[0]:lim[1]]
		fig.add_trace(go.Scattergeo(
			lon = df_sub['lon'],
			lat = df_sub['lat'],
			marker = dict(
				size = df_sub['y'].fillna(0)/scale,
				color = colors[i],
				line_color='rgb(40,40,40)',
				line_width=0.5,
				sizemode = 'area'
		),
		name = '{0} - {1}'.format(lim[0],lim[1]))
		)

	fig.update_geos(
		visible=False,
		projection_type="mercator",
		lataxis_range=[49, 55],
		lonaxis_range=[14, 24],
	)

	fig.update_layout(
		title_text = 'Poland',
		showlegend = True,
		geo = dict(
			scope = 'europe',
		),
		height=700
	)
	return fig

