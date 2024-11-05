import unittest
import pandas as pd
import os
import logging
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from data_preprocessing import DataPreprocessor

# Define constants for the test
TEST_DATA_DIR = "../data/"
TEST_DATA_FILE = "test_data.csv"
TEST_DATA_PATH = os.path.join(TEST_DATA_DIR, TEST_DATA_FILE)

# Create a sample DataFrame for testing
sample_data = {
    "Date": ["2021-01-01", "2021-01-02", "2021-01-03"],
    "Sales": [100, 200, 150],
    "Customers": [10, 20, 15],
    "Open": [1, 1, 1],
    "Promo": [1, 0, 1]
}

class TestDataPreprocessor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up logging for the test
        logging.basicConfig(level=logging.INFO)
        cls.logger = logging.getLogger("TestLogger")

        # Create test data directory if it doesn't exist
        os.makedirs(TEST_DATA_DIR, exist_ok=True)

        # Create a sample CSV file for testing
        sample_df = pd.DataFrame(sample_data)
        sample_df.to_csv(TEST_DATA_PATH, index=False)

    @classmethod
    def tearDownClass(cls):
        # Clean up the test data file after tests are done
        if os.path.exists(TEST_DATA_PATH):
            os.remove(TEST_DATA_PATH)

    def setUp(self):
        # Initialize DataPreprocessor with the test data path
        self.preprocessor = DataPreprocessor(data_path=TEST_DATA_PATH, logger=self.logger)

    def test_load_data(self):
        """Test if the data loads correctly from a local file."""
        data = self.preprocessor.load_data()
        self.assertIsInstance(data, pd.DataFrame, "Loaded data is not a DataFrame.")
        self.assertEqual(data.shape[0], len(sample_data["Date"]), "Number of rows in loaded data does not match.")
        self.assertEqual(data.shape[1], len(sample_data.keys()), "Number of columns in loaded data does not match.")

    def test_inspect_data(self):
        """Test the inspect method on a loaded DataFrame."""
        data = self.preprocessor.load_data()
        # We don't expect the inspect method to raise any errors for valid data
        try:
            self.preprocessor.inspect(data)
        except Exception as e:
            self.fail(f"inspect method raised an exception: {e}")

    def test_load_data_file_not_found(self):
        """Test load_data method for handling file not found error."""
        invalid_preprocessor = DataPreprocessor(data_path="../data/invalid_file.csv", logger=self.logger)
        with self.assertRaises(FileNotFoundError):
            invalid_preprocessor.load_data()

    def test_inspect_empty_dataframe(self):
        """Test inspect method for handling an empty DataFrame."""
        empty_df = pd.DataFrame()
        with self.assertRaises(ValueError):
            self.preprocessor.inspect(empty_df)

if __name__ == "__main__":
    unittest.main()
