# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from data import get_data_as_df, DATA, get_max_value_keys
from plots import create_spider_plot, create_bar_plot,geo_plot

product_choice = 'Juice'

app = Dash(__name__, external_stylesheets=[
	dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME,
	"https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css"
])
categories = ['age', 'poi']
products = ['Juice', 'Apples', 'Snackbar']

def graph_plot(data, category: str)->dcc.Graph:
	is_multi = len(data[data['category']==category]['subcategory'].unique()) > 2
	# return html.Div([
	return dcc.Graph(
			figure=create_spider_plot(data, category) if is_multi else create_bar_plot(data, category),
		)
		# html.Div(category.capitalize().replace("_", " "))
	# ], style={'textAlign': 'center', 'margin': '0 auto'})

def target_description(data):
	return f'''
### Possible Target Group

{
	'\n\n'.join(f'**{k.capitalize().replace("_", " ")}**: {v}'
				for k,v in get_max_value_keys(data).items()
				)
	}
'''
def create_card(icon_class, text, number, color):
	return dbc.Card(
		[
			dbc.Row(
				[
					dbc.Col(
						html.I(className=icon_class, style={"color": color, 'font-size': '4rem'}),
						className="d-flex justify-content-center align-items-center",
					),
					dbc.Col(
						dbc.CardBody(
							[
								html.H4(text, className="card-title"),
								html.P(
									number,
									className="card-text",
								),
							]
						),
						className="col-md-8",
					),
				],
				className="g-0 d-flex align-items-center",
			)
		],
		className="mb-3",
		style={"maxWidth": "540px"},
	)

# Define four cards
app.layout = html.Div([
	dbc.Row([
		dbc.Row([
			dbc.Col([
				dbc.Label('Product'),
				dcc.Dropdown(products, products[0], id='product-selection')]),
			dbc.Col(dcc.DatePickerRange()),
		], justify="between", align='end'),
		dbc.Row(id='cards-id', className='gy-2'),
	]),
	dbc.Row(id='best-values')
], style={'padding': '1% 5%'})

@callback(
	Output(component_id='best-values', component_property='children'),
	Input(component_id='product-selection', component_property='value')
)
def update_graph(col_chosen):
	data = get_data_as_df(DATA[col_chosen])
	graphs = [graph_plot(data, category) for category in data['category'].unique()]
	return dbc.Row([
		dbc.Col([dcc.Graph(
			figure=geo_plot()
		),]),
		dbc.Col([
			dbc.Row([
				dbc.Col(graphs[0]),
				dbc.Col(graphs[1])
			]),
			dbc.Row([
				dbc.Col(graphs[2]),
				dbc.Col(graphs[3])
			]),
		])
	])

@callback(
	Output(component_id='cards-id', component_property='children'),
	Input(component_id='product-selection', component_property='value')
)
def update_graph(col_chosen):
	data = get_data_as_df(DATA[col_chosen])
	res=data.loc[data.groupby('category')['value'].idxmax(), ['category', 'subcategory']]
	res=res.set_index('category')['subcategory'].to_dict()
	return html.Div([
		dbc.Row([
			dbc.Col(create_card("bi bi-people", "Wiek", res.get('age'), "#007bff"), width=3),
			dbc.Col(create_card("bi bi-cash", "POI", res.get('poi'), "#28a745"), width=3),
			dbc.Col(create_card("bi bi-people", "Users", "1,500", "#17a2b8"), width=3),
			dbc.Col(create_card("bi bi-activity", "Engagement", "65%", "#ffc107"), width=3),
		], justify="around")
	])

if __name__ == '__main__':
	app.run(debug=True)
