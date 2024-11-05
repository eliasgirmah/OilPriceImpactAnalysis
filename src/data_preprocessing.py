import pandas as pd
import os
import logging

class DataPreprocessor:
    def __init__(self, file_path: str, logger: logging.Logger = None):
        """
        Initialize the DataPreprocessor class with the path to the dataset.
        
        Parameters:
        file_path (str): The path to the local data file.
        logger (logging.Logger): Logger for tracking events and errors.
        """
        self.file_path = file_path
        self.data: pd.DataFrame = None
        self.logger = logger if logger else logging.getLogger(__name__)

    def load_data(self) -> pd.DataFrame:
        """
        Load the dataset from a local path into a pandas DataFrame.
        
        Returns:
        pd.DataFrame: The loaded dataset.
        """
        try:
            # Log the data loading attempt
            self.logger.info("Starting to load data from the local file path.")
            
            # Load data into a pandas DataFrame
            self.data = pd.read_csv(self.file_path)
            
            # Convert the 'Date' column to datetime format if it exists
            if 'Date' in self.data.columns:
                self.data['Date'] = pd.to_datetime(self.data['Date'].str.strip(), errors='coerce')
                self.logger.info("Converted 'Date' column to datetime format.")

            self.logger.info("Data loaded into DataFrame successfully.")
            return self.data
        except Exception as e:
            self.logger.error(f"Error loading data: {e}")
            raise

    def inspect(self, df: pd.DataFrame) -> None:
        """
        Inspect the given DataFrame for structure, completeness, and summary statistics.

        Parameters:
        - df (pd.DataFrame): The DataFrame to inspect.
        """
        if df.empty:
            self.logger.error("The DataFrame is empty.")
            raise ValueError("The DataFrame is empty.")

        try:
            # Dimensions of the DataFrame
            dimensions = df.shape
            print(f"Dimensions (rows, columns): {dimensions}")
            self.logger.info(f"DataFrame dimensions: {dimensions}")

            # Data types of each column
            data_types = df.dtypes
            print("\nData Types:")
            print(data_types)
            self.logger.info("Displayed data types for each column.")

            # Missing values in each column
            missing_values = df.isnull().sum()
            print("\nMissing Values:")
            print(missing_values[missing_values > 0])
            if missing_values.any():
                self.logger.warning("Missing values found.")
            else:
                self.logger.info("No missing values detected.")

            # Unique values in each column
            unique_values = df.nunique()
            print("\nUnique Values in Each Column:")
            print(unique_values)

            # Count of duplicate rows
            duplicate_count = df.duplicated().sum()
            print(f"\nNumber of duplicate rows: {duplicate_count}")
            self.logger.info(f"Duplicate rows found: {duplicate_count}")

            # Display duplicate rows if any
            if duplicate_count > 0:
                duplicates = df[df.duplicated()]
                print("\nDuplicate rows:")
                print(duplicates)

            # Summary statistics for numeric columns
            summary_statistics = df.describe(include='number')
            print("\nSummary Statistics for Numeric Columns:")
            print(summary_statistics)

            self.logger.info("Data inspection completed successfully.")
        except Exception as e:
            self.logger.error(f"An error occurred during inspection: {e}")
            raise
