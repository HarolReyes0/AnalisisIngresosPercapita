from modeling.data_cleaning import ModelData
from dashboard.layout import load_data, show_dashboard

def main():
    # Modeling and saving the data.
    data_modeler = ModelData()
    data_modeler.model_and_save_data()

    # Loading the data.
    load_data()

    # Displaying the dashboard.
    show_dashboard()

if __name__ == '__main__':
    main()