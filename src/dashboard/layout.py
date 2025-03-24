from dash import dcc, html, Dash
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from charts import *
from dash.dependencies import Input, Output

def load_data():
    """
        Loads and processes Excel datasets from predefined file paths, and sets global variables.

        This function performs the following tasks:
        - Loads three Excel files into global DataFrames: `one0`, `one1`, and `one2`.
        - Sets a global float display format to two decimal places for all pandas DataFrames.
        - Extracts all unique years from the 'año' column across the three datasets and stores them 
        in a global set variable `available_years`.

        Global Variables:
        - one0 (pd.DataFrame): Data loaded from 'one 0.xlsx'.
        - one1 (pd.DataFrame): Data loaded from 'one 1.xlsx'.
        - one2 (pd.DataFrame): Data loaded from 'one 2.xlsx'.
        - available_years (set): Set of all unique years found in the 'año' column across all three datasets.

        Note:
            The function assumes the Excel files are located relative to the script path at:
            '../../data/processed/one/' and each file contains a column named 'año'.
    """
    global one0, one1, one2, available_years

    # Reading all files
    one0 = pd.read_excel('data/processed/one/one 0.xlsx')
    one1 = pd.read_excel('data/processed/one/one 1.xlsx')
    one2 = pd.read_excel('data/processed/one/one 2.xlsx')
    
    pd.options.display.float_format = '{:.2f}'.format

    # Obtaining the list of available years.
    available_years = {int(x) for df in [one0, one1, one2] for x in df['año'].unique().tolist()}



def show_dashboard():
    # Creating the dashboard layout.
    dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

    load_figure_template('COSMO')

    app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO, dbc_css])

    app.layout = dbc.Container([
        html.H1('Ingresos por Capitas'),
        # Slicer to filter the years.
        dbc.Row([
            dbc.Col([
                html.H1("Año"),
                dcc.RangeSlider(
                    id='YearPicker',
                    min=min(available_years),
                    max=max(available_years),
                    step=1,
                    value=[min(available_years), max(available_years)],
                    # show marks every 2 years
                    marks={year: str(year) for year in available_years if year % 2 == 0}
                ), 
            ]),
            # Radio buttons to filter the regime type.
            dbc.Col([
                html.H1('Tipo de Afiliado'),
                dcc.RadioItems(
                    id='RegimeType',
                    options=[
                        {'label': 'Subsidiado', 'value': 'Subsidiado'},
                        {'label': 'Contributivo', 'value': 'Contributivo'},
                        {'label': 'Todos', 'value': 'Todos'}
                    ],
                    value='Todos',
                    labelStyle={
                        'display': 'inline-block',
                        'margin-right': '15px',
                    }
                ),
            ])
        ]),
        # Adding charts
        dbc.Row([
            dcc.Graph(id='AffiliatePerYear'),
            # Creating rows and columns to separate the charts.
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='CapitalizationPerCustType'),
                ]),
                dbc.Col([
                    dcc.Graph(id='CapitalizationPerGender'),
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='AmtCapitationsPerCustType'),
                ]),
                dbc.Col(
                    dcc.Graph(id='MoneyCollectedPerCustType')
                )
            ]),
        ]),
    ])

    @app.callback(
            [
                Output('AffiliatePerYear', 'figure'), 
                Output('CapitalizationPerCustType', 'figure'), 
                Output('CapitalizationPerGender', 'figure'), 
                Output('AmtCapitationsPerCustType', 'figure'),
                Output('MoneyCollectedPerCustType', 'figure')
            ],
            [
                Input('RegimeType', 'value'),
                Input('YearPicker', 'value'),
            ]
    )
    def create_charts(filter_: str, years: list) -> None:
        """
            Generates a collection of charts based on provided filter and years.

            This function creates multiple visualizations using pre-loaded datasets (`one0`, `one1`, `one2`)
            and a the typer of regime and list of years. Each chart corresponds to a specific aspect of the data.

            Parameters:
            - filter_ (str): A string filter used to segment or filter the data.
            - years (list): A list of years (int) used to filter the data before generating the charts.

            Returns:
            - tuple: A tuple containing the generated figures in the following order.
        """
        # Creating the range of years.
        years = [year for year in range(int(years[0]), int(years[1]) + 1, 1)]

        # Constructing all charts.
        figs = (
            cust_amt_per_capitation_type(one0, filter_, years),
            amt_capitation_paid_per_cust_type(one0, filter_, years),
            amt_capitation_per_gender(one1, filter_, years),
            capitation_amt_per_cust_type(one2, years),
            pct_money_per_cust_type(one2, years),
        )

        return figs

    app.run(jupyter_mode='tab', port=8071)

if __name__ == '__main__':
    load_data()
    show_dashboard()