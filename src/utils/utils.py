import pandas as pd
import numpy as np
from typing import List

def model_ONE_data(path: str) -> pd.DataFrame:
    """
        Reads and processes a dataset from an Excel or CSV file, transforming it into a structured DataFrame.

        The function:
        1. Reads the data from the provided file path, attempting to load it as an Excel file first and falling back to CSV if necessary.
        2. Removes unwanted rows from the beginning and end of the dataset.
        3. Iterates through the rows to dynamically generate column names based on non-null values in the first column.
        4. Ensures column names are unique by appending an index if duplicates exist.
        5. Transposes the processed data and removes the index column.

        Parameters:
        paths : str
            The file path of the dataset to be loaded. The function supports `.xlsx` and `.csv` formats.

        Returns:
        pd.DataFrame
            A transformed DataFrame where the original data is transposed, and column names are dynamically generated.
        
        Raises:
        ValueError
            If the file format is invalid or unreadable.
    """
    raw_column_name = ''
    # Reading the data.
    try:
        data = pd.read_excel(path, engine='openpyxl')
    except ValueError:
        data = pd.read_csv(path).reset_index(drop=True)

    # Finding the start of our data.
    try:
        index_ = list(data.iloc[:,0].str.lower()).index('años')
    except ValueError:
        index_ = list(data.iloc[:,0].str.lower()).index('año')

    # Filtering the unwanted rows
    data = data.iloc[index_:-3]
    
    # Iterating over the data rows.
    for i in range(data.shape[0]):
        # If the cell is not a null value is considered as a valid title.
        if pd.notna(data.iloc[i, 0]):
            raw_column_name = data.iloc[i, 0]
        
        # Creating the column name.
        column_name = f'{raw_column_name} ({data.iloc[i, 1]})'

        # If column name exist add an index number to differentiate it from the other columns.
        if column_name in data.iloc[:, 1].values: 
            column_name += f' {i}'

        # Title is added to the sub title to have the column name.
        data.iloc[i, 1] = column_name
        
    # Transposing and filtering the data.
    data = data.iloc[:, 1:].T.reset_index(drop=True)

    # Obtaining the column headers.
    headers = data.iloc[0]
    # Replacing the headers.
    data.columns = headers

    # # Dropping unwanted rows.
    data.drop(labels=0, inplace=True)
    
    # Filling the missing years.
    data.iloc[:, 0] = data.iloc[:, 0].fillna(method='ffill')
    
    # Filtering rows.
    data = data[(data.iloc[:, 1].str.strip() == 'Cuarto trimestre') | (data.iloc[:, 1].isna())]

    # Dropping unwanted columns
    try:
        data.drop('Años (nan) 1', axis=1, inplace=True)
    except KeyError:
        data.drop('Año (nan) 1', axis=1, inplace=True)

    # Cleaning extra characters.
    data.iloc[:, 0] = data.iloc[:, 0].astype(str).str.replace('*', '', regex=False).astype(float)
    
    return data

def model_CNSS_data(paths: List[str]) -> pd.DataFrame:
    """
        Processes multiple Excel or CSV files containing CNSS data, standardizes column names, merges them, 
        and extracts year and month information.

        The function performs the following steps:
        1. Reads multiple data files (Excel or CSV) from the provided paths.
        2. Standardizes column names by converting them to lowercase and replacing "meses" with "mes".
        3. Creates a new "fecha" column by combining "año" and "mes" as a string.
        4. Drops the original "año" and "mes" columns after creating "fecha".
        5. Merges all processed dataframes on the "fecha" column.
        6. Splits "fecha" into separate "año" (year) and "mes" (month) columns.
        7. Drops the "fecha" column before returning the final processed dataframe.

        Parameters:
        *kargs : tuple
            A tuple containing a list of file paths to Excel (.xlsx) or CSV (.csv) files.

        Returns:
        pd.DataFrame
            A cleaned and merged dataframe with standardized column names and separate "año" and "mes" columns.

        Raises:
        ValueError:
            If a file cannot be read as an Excel or CSV file.
        KeyError:
            If required columns ("año", "mes") are missing in any dataframe.
    """
    raw_dataframes = []
    processed_dataframes = []
    
    # Reading and appending all dataframes.
    for path in paths:
        try:
            data = pd.read_excel(path, engine='openpyxl')
        except ValueError:
            data = pd.read_csv(path)
        
        # Saving the data in memory.
        raw_dataframes.append(data)

    for dataframe in raw_dataframes:
        # Standardizing columns names.
        columns = ['mes' if column.lower().strip() == 'meses' else column.lower().strip() for column in dataframe.columns]
        # Updating the columns names.
        dataframe.columns = columns
        # Creating a new column combining the year and month.
        dataframe['fecha'] = dataframe['año'].astype('str') + ' ' + dataframe['mes']

        # Dropping the month and year
        dataframe.drop(['año', 'mes'], axis=1, inplace=True)

        processed_dataframes.append(dataframe)
    
    # Merging the data.
    data = processed_dataframes[0]
    
    for dataframe in processed_dataframes[1:]: 
        data = pd.merge(data, dataframe, on='fecha')

    # Splitting the date into year and month.
    data[['año', 'mes']] = data['fecha'].str.split(' ', expand=True, n=1)

    # Dropping "date" columns.
    data.drop('fecha', axis=1, inplace=True)
    
    return data

def model_all_data() -> dict:
    """
        Models data from multiple sources and returns a structured dictionary.

        This function retrieves raw data files from predefined directories ('ONE' and 'CNSS'), 
        processes them using respective modeling functions (`model_ONE_data` and `model_CNSS_data`), 
        and returns the structured data.

        Returns:
            dict: A dictionary containing the modeled data for 'ONE' and 'CNSS'. 
                - 'ONE': A list of modeled data from individual files in the '../data/raw/one' directory.
                - 'CNSS': A single entry containing the modeled data from the '../data/raw/cnss' directory.

    """
    data_modeled = {
    'ONE' : [],
    'CNSS' : [],
    }

    # Obtaining all data paths.
    paths = {
    'ONE': [os.path.join('../data/raw/one', path) for path in os.listdir('../data/raw/one')],
    'CNSS': [os.path.join('../data/raw/cnss', path) for path in os.listdir('../data/raw/cnss')],
    }

    # Modeling all data from the ONE.
    for path in paths.get('ONE'):
        data = model_ONE_data(path)

        data_modeled.get('ONE').append(data)
    
    # Modeling all data from CNSS.
    data_modeled.get('CNSS').append(model_CNSS_data(paths['CNSS']))

    return data_modeled

if __name__ == '__main__':
    ONE_data_path = 'data/Raw Data/afiliados-número-cápitas-cápitas-pagadas-sfs-según-régimen-2005-2023.xlsx'
    
    data = model_ONE_data(ONE_data_path)

    print(data)

    CNSS_data_paths = [
        'data/Raw Data/Excel-–-Regimen-Contributivo-Recaudos-y-Pagos-Seguro-Familiar-de-Salud-Seguros-Julio-2003-a-Noviembre-2024.xlsx',
        'data/Raw Data/Excel-–-Regimen-Subsidiado-Aportes-Pagos-Seguro-Familiar-de-Salud-Enero-2004-octubre-2024-a-Noviembre-2024-1.xlsx'
        ]
    
    data = model_CNSS_data(CNSS_data_paths)

    print(data)