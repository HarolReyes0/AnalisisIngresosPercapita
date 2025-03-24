from dash import dcc, html, Dash
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from charts import *


def load_data():
    global one0, one1, one2, available_years

    one0 = pd.read_excel('../../data/processed/one/one 0.xlsx')
    one1 = pd.read_excel('../../data/processed/one/one 1.xlsx')
    one2 = pd.read_excel('../../data/processed/one/one 2.xlsx')
    
    pd.options.display.float_format = '{:.2f}'.format

    available_years = {(x) for df in [one0, one1, one2] for x in df['año'].unique().tolist()}

def create_charts(filter_: str, years: list) -> None:
    pass

def show_dashboard():
    # Creating the dashboard layout.
    dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

    load_figure_template('COSMO')

    app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO, dbc_css])

    app.layout = html.Div([
        html.H1('Ingresos por Capitas'),
            dbc.Row([
                dbc.Card([
                    dbc.Col([
                        # Creating a slicer to filter the years.
                        html.H1("Año"),
                        dcc.Slider(
                            id='YearPicker',
                            min=min(available_years),
                            max=max(available_years),
                            step=1,
                            value=[],
                            # show marks every 2 years
                            marks={year: str(year) for year in available_years if year % 2 == 0}
                        ),  
                    ], width=5),
                    dbc.Col([
                        # Creating a dropdown to filter the regime type.
                        html.H1('Tipo de Afiliado'),
                        dcc.RadioItems(
                            id='RegimeType',
                            options=['Subsidiado', 'Contributivo', 'Todos'],
                            value='todos'
                        ),
                    ]),
                ])
        ]),
        
        # Adding charts
        dcc.Graph(id='AffiliatePerYear'),
        dcc.Graph(id='CapitalizationPerCustType'),
        dcc.Graph(id='CapitalizationPerGender'),
        dcc.Graph(id='AmtCapitationsPerCustType'),
        dcc.Graph(id='MoneyCollectedPerCustType')
    ])

    app.run(jupyter_mode='tab', port=8071)

if __name__ == '__main__':
    load_data()
    show_dashboard()