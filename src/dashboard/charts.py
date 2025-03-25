import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def cust_amt_per_capitation_type(data: pd.DataFrame, filter_: str, years=[]) -> go.Figure:
    """
        Generates a line plot showing customer amounts based on capitation type over specified years.

        Parameters
        data : pd.DataFrame
            A DataFrame containing at least the columns 'año', 'afiliados (total)', 
            'afiliados (subsidiado)', and 'afiliados (contributivo)'.
        filter_ : str
            A string that determines which capitation type(s) to visualize.
            Acceptable values are:
                - 'subsidiado': plots only 'afiliados (subsidiado)'
                - 'contributivo': plots only 'afiliados (contributivo)'
                - Any other value defaults to plotting all three categories.
        years : list, optional
            A list of years (integers) to filter the data by. If the list is empty, all years are included.

        Returns
        plotly.graph_objects.Figure
            A line plot figure object showing the selected data.

        Raises
        ValueError
            If `years` is not a list.
        ValueError
            If the specified years are not present in the dataset.
    """
    # Raising an error if years is not a list
    if type(years) is not list:
        raise ValueError('years must be a list.')
    
    # Raising an error if the years selected are not found.
    if not any(data['año'].isin(years)) and len(years) > 0:
        raise ValueError('years entered not found in the data.')
    
    # Filtering the data by selected years if year is in the data.
    if set(set(years)).issubset(data['año']) and len(years) > 0:
        data = data.loc[data['año'].isin(years)]

    # Data filters.
    default_filter = {
        'afiliados (total)': 'Todos',
        'afiliados (subsidiado)': 'Subsidiado',
        'afiliados (contributivo)': 'Contributivo'
    }
    filters = {
        'Subsidiado' : {'afiliados (subsidiado)': 'Subsidiado'},
        'Contributivo' : {'afiliados (contributivo)': 'Contributivo'},
    }

    # Selecting the data that will be used as y axis.
    axis_and_labels = filters.get(filter_, default_filter)

    # Plotting the data.
    fig = px.line(
        data_frame = data,
        x = 'año',
        y = list(axis_and_labels.keys()),
        markers=True,
        title='Cantidad de Afiliados',
        labels={'value': '', 'variable':'Tipo de Regimen'}
    )

    # Updating the legend.
    fig.for_each_trace(
        lambda t: t.update(name=axis_and_labels.get(t.name, t.name))
    )
    return fig

def amt_capitation_paid_per_cust_type(data: pd.DataFrame, filter_: str, years=[]) -> go.Figure:
    """
        Generates a bar chart showing the number of capitation payments made per customer type over specified years.

        Parameters
        data : pd.DataFrame
            A DataFrame containing at least the columns:
            'año', 'numero de cápitas pagadas (subsidiado)', and 'numero de cápitas pagadas (contributivo)'.
        filter_ : str
            A string indicating which customer type to filter by. Acceptable values are:
                - 'subsidiado': shows only 'numero de cápitas pagadas (subsidiado)'
                - 'contributivo': shows only 'numero de cápitas pagadas (contributivo)'
                - Any other value defaults to showing both.
        years : list, optional
            A list of years (integers) to filter the data by. If empty, all years in the dataset are used.

        Returns
        plotly.graph_objects.Figure
            A bar chart figure object displaying the number of capitation payments per year.

        Raises
        ValueError
            If `years` is not a list.
        ValueError
            If none of the specified years are found in the data.
    """
    
    # Raising an error if years is not a list
    if type(years) is not list:
        raise ValueError('years must be a list.')
    
    # Raising an error if the years selected are not found.
    if not any(data['año'].isin(years)) and len(years) > 0:
        raise ValueError('years entered not found in the data.')

    # Filtering the data by selected years if year is in the data.
    if set(set(years)).issubset(data['año']) and len(years) > 0:
        data = data.loc[data['año'].isin(years)]
    
    # Data filters.
    default_filter = {
        'numero de cápitas pagadas (subsidiado)': 'Subsidiado',
        'numero de cápitas pagadas (contributivo)': 'Contributivo'
    }
    filters = {
        'Subsidiado' : {'numero de cápitas pagadas (subsidiado)': 'Subsidiado'},
        'Contributivo' : {'numero de cápitas pagadas (contributivo)': 'Contributivo'},
    }

    # Selecting the data that will be used as y axis.
    axis_and_labels = filters.get(filter_, default_filter)

    # Plotting the data.
    fig = px.bar(
        data,
        x='año',
        y= list(axis_and_labels.keys()),
        title='Numero de cápitas pagadas',
        labels={'value': '', 'variable':'Tipo de Regimen'}
    )

    # Updating the legend.
    fig.for_each_trace(
        lambda t: t.update(name=axis_and_labels.get(t.name, t.name))
    )

    return fig

def amt_capitation_per_gender(data: pd.DataFrame, filter_: str, years=[]) -> go.Figure:
    """
        Generates a grouped bar chart showing the amount of capitation per gender over specified years.

        Parameters
        data : pd.DataFrame
            A DataFrame containing at least the columns:
            - 'año'
            - 'total  (hombres)', 'total  (mujeres)'
            - 'régimen subsidiado (hombres )', 'régimen subsidiado (mujeres )'
            - 'régimen contributivo (hombres )', 'régimen contributivo (mujeres )'
        filter_ : str
            A string that specifies the capitation type to filter by. Accepted values are:
                - 'subsidiado': plots only 'régimen subsidiado' by gender.
                - 'contributivo': plots only 'régimen contributivo' by gender.
                - Any other value defaults to plotting the total by gender.
        years : list, optional
            A list of years (integers) to filter the data. If empty, all years are included.

        Returns
        go.Figure
            A Plotly grouped bar chart showing the amount of capitation per gender by year.

        Raises
        ValueError
            If `years` is not a list.
        ValueError
            If the provided years are not found in the DataFrame.
    """
    if type(years) is not list:
        raise ValueError('years must be a list.')
    
    # Raising an error if the years selected are not found.
    if not any(data['año'].isin(years)) and len(years) > 0:
        raise ValueError('years entered not found in the data.')
    
    # Filtering the data by selected years if year is in the data.
    if set(set(years)).issubset(data['año']) and len(years) > 0:
        data = data.loc[data['año'].isin(years)]
    
    # Data filters.
    default_filter = {
        'total  (hombres)': 'Hombres',
        'total  (mujeres)': 'Mujeres'
    }
    filters = {
        'Subsidiado' : {'régimen subsidiado (hombres )': 'Hombres', 'régimen subsidiado (mujeres )': 'Mujeres',},
        'Contributivo' : {'régimen contributivo (hombres )': 'Hombres', 'régimen contributivo (mujeres )': 'Mujeres',},
    }

    # Selecting the data that will be used as y axis.
    axis_and_labels = filters.get(filter_, default_filter)

    # Plotting the data.
    fig = px.bar(
        data,
        x='año',
        y=list(axis_and_labels.keys()),
        barmode='group',
        title=f'Capitas Dispersadas por Genero',
        labels={'value':'', 'variable':'Genero'}
    )
    # Updating the legend.
    fig.for_each_trace(
        lambda t: t.update(name=axis_and_labels.get(t.name, t.name))
    )

    return fig

def capitation_amt_per_cust_type(data: pd.DataFrame, years=[]) -> go.Figure:
    """
        Generates a line plot of capitation amounts by customer type, filtered by year(s) and month.

        The function visualizes the number of capitation disbursements for different customer types 
        (total, titulares, direct dependents, and additional dependents) using a line chart. 
        It filters the data based on the provided years, focusing on December by default. 
        If only one year is selected, the data is shown by month.

        Args:
            data (pd.DataFrame): Input DataFrame containing at least the following columns:
                - 'año': year of the record.
                - 'meses': month name in Spanish (e.g., 'enero', 'febrero', etc.).
                - Columns with capitation data (e.g., ' número de cápitas dispersadas(total)').
            years (list, optional): List of years to filter the data. Defaults to an empty list,
                which uses the most recent December.

        Returns:
            go.Figure: A Plotly line chart object showing capitation trends by customer type.

        Raises:
            ValueError: If `years` is not a list.
            ValueError: If provided years are not found in the dataset.
    """
    months = {
        'enero': 1,
        'febrero': 2,
        'marzo': 3,
        'abril': 4,
        'mayo': 5,
        'junio': 6,
        'julio': 7,
        'agosto': 8,
        'septiembre': 9,
        'octubre': 10,
        'noviembre': 11,
        'diciembre': 12,
    }
    x_axis = 'año'

    # Raising an error if years is not a list
    if type(years) is not list:
        raise ValueError('years must be a list.')
    
    if len(years) == 1 and not any(data['año'].isin(years)):
        raise(ValueError('Year not found in the data.'))

    # If only one year was selected, filtering the data by month.
    if len(years) == 1:
        x_axis = 'meses'
        # Filtering by the selected year.
        data = data.loc[data['año'].isin(years)]
        # Standardizing months names. 
        data['meses'] = data['meses'].str.strip().str.lower()
        # Mapping the months to numbers.
        data['meses_n'] = data['meses'].map(months)

        # Sorting the months in ascending order.
        data.sort_values(by='meses_n')
    else:
        data = data.loc[data['meses'].str.strip() == 'Diciembre', :]

        # Filtering the years selected only by the ones found in the data.
        if not any(data['año'].isin(years)) and len(years) > 0:
            years = list(set(data['año'].tolist()).intersection(set(years)))
            print(years)
        
        data = data.loc[data['año'].isin(years)]
    
    # Data filters.
    default_filter = [' número de cápitas dispersadas(total)', ' número de cápitas dispersadas (titulares)', ' número de cápitas dispersadas (dependientes directos)',
        ' número de cápitas dispersadas (dependientes adicionales)']
    filters = {
    }

    # Selecting the data that will be used as y axis.
    y_axis_data = filters.get('', default_filter)

    # Plotting the data.
    fig = px.line(
        data_frame = data,
        x = x_axis,
        y = y_axis_data,
        markers=True
    )

    return fig
    
def pct_money_per_cust_type(data: pd.DataFrame, years=[]) -> go.Figure:
    """
        Generate a stacked bar chart of the percentage of total disbursed amounts by customer type 
        (titulares, dependientes directos, and dependientes adicionales).

        The function filters the data to include only rows where 'meses' is "Diciembre", 
        optionally filters by the given list of years, calculates the percentage of the total 
        disbursed amount for each customer type, and returns a Plotly Figure of the resulting data.

        Parameters
        data : pd.DataFrame
            A DataFrame containing at least the following columns:
                - 'año': Year of the record (integer or string).
                - 'meses': Month of the record (string).
                - 'dependientes directos': Disbursed amount for direct dependents.
                - 'titulares': Disbursed amount for titular customers.
                - 'dependientes adicionales': Disbursed amount for additional dependents.
                - 'total de monto dispersado RD$ (Total)': Total disbursed amount.
        years : list, optional
            A list of years (as integers or strings) to filter the data. 
            If empty, all years present in the DataFrame are included. 
            Default is [] (no filtering by year).

        Raises
        ValueError
            If 'years' is not a list, or if any of the provided years are not found in the data.

        Returns
        go.Figure
            A Plotly Figure object displaying a stacked bar chart where:
            - The y-axis shows the years (as strings).
            - The x-axis represents the percentage of the total disbursed amount.
            - The bars are stacked for titulares, dependientes directos, and dependientes adicionales.
    """
    # Raising an error if years is not a list
    if type(years) is not list:
        raise ValueError('years must be a list.')
    
    # Raising an error if the years selected are not found.
    if not any(data['año'].isin(years)) and len(years) > 0:
        raise ValueError('years entered not found in the data.')

    # Filtering the data by selected years if year is in the data.
    if set(set(years)).issubset(data['año']) and len(years) > 0:
        data = data.loc[data['año'].isin(years)]
        data = data.loc[data['meses'].str.strip() == 'Diciembre', :]
    
    # Calculating the percentages.
    for column in ['dependientes directos', 'titulares', 'dependientes adicionales']:
        data[f'total de monto dispersado RD$ ({column}) %'] = round((data[f'total de monto dispersado RD$ ({column})']/
            data['total de monto dispersado RD$ (Total)']) * 100, 2)
    
    # Filtering the data to extract the data from december.
    data = data.loc[data['meses'].str.strip() == 'Diciembre', :]

    data['año'] = data['año'].astype('str')

    # Creating the figure.
    fig = px.bar(
    data,
    y='año',
    x=['total de monto dispersado RD$ (titulares) %',
    'total de monto dispersado RD$ (dependientes directos) %',
    'total de monto dispersado RD$ (dependientes adicionales) %'],
       barmode='stack',
    )

    return fig