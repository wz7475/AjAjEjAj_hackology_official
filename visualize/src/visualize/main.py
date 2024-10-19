# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from data import get_data_as_df, DATA, get_max_value_keys
from plots import create_spider_plot, create_bar_plot

product_choice = 'Juice'

app = Dash(__name__, external_stylesheets=[
	"https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap"
])
categories = ['age', 'poi']
products = ['Juice', 'Apples', 'Snackbar']

def graph_plot(data, category: str)->html.Div:
	is_multi = len(data[data['category']==category]['subcategory'].unique()) > 2
	return html.Div([
		dcc.Graph(
			figure=create_spider_plot(data, category) if is_multi else create_bar_plot(data, category),
		),
		html.Div(category.capitalize().replace("_", " "))
	], style={'textAlign': 'center', 'margin': '0 auto'})

def target_description(data):
	return f'''
### Possible Target Group

{
	'\n\n'.join(f'**{k.capitalize().replace("_", " ")}**: {v}'
				for k,v in get_max_value_keys(data).items()
				)
	}
'''

app.layout = html.Div([
	html.Div([
		html.Label('Products'),
		dcc.Dropdown(products, products[0], id='product-selection'),
		html.Br(),
		dcc.DatePickerRange(),
	], style={'justify-content':'center'}),
	html.Div(id='best-values')


], style={'padding': '0 5%'})

# Adding custom scrollbar CSS
# # Add controls to build the interaction
@callback(
	Output(component_id='best-values', component_property='children'),
	Input(component_id='product-selection', component_property='value')
)
def update_graph(col_chosen):
	data = get_data_as_df(DATA[col_chosen])
	return html.Div([
		html.Div(children=[
			dcc.Markdown(target_description(DATA[col_chosen])),
		], style={'padding': 10, 'flex': 1}),

		html.Div(children=[
			graph_plot(data, category) for category in data['category'].unique()
		], style={'padding': 0, 'flex': 2, 'display': 'grid', 'grid-template-columns': 'auto auto'})
	],
		# style={'display': 'flex', 'flexDirection': 'row', },
		className='responsive-layout')

# Run the app
if __name__ == '__main__':
	app.run(debug=True)
