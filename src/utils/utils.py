import pandas as pd
import numpy as np

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
        path : str
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
        data = pd.read_csv(path)

    # Filtering the unwanted rows
    data = data.iloc[2:-3]
    
    # Iterating over the data rows.
    for i in range(data.shape[0]):
        # If the cell is not a null value is considered as a valid title.
        if data.iloc[i, 0] is not np.nan:
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
    
    return data

if __name__ == '__main__':
    ONE_data_path = 'data/Raw Data/afiliados-número-cápitas-cápitas-pagadas-sfs-según-régimen-2005-2023.xlsx'
    
    data = model_ONE_data(ONE_data_path)

    print(data)