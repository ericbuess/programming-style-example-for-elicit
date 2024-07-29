import pandas as pd
import numpy as np
from scipy import stats
import logging
from typing import Dict, Any, Optional
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
from dataclasses import dataclass

# Load environment variables
load_dotenv()

# Configure logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')

@dataclass
class Statistics:
    mean: pd.Series
    median: pd.Series
    mode: pd.Series

class DataProcessor:
    """
    A class used to process data, compute basic statistics, and visualize data.

    Attributes
    ----------
    data : Optional[pd.DataFrame]
        The loaded data.
    statistics : Dict[str, Any]
        Computed statistics of the data.

    Methods
    -------
    load_data(file_path: str) -> None
        Loads data from a CSV file.
    compute_statistics() -> None
        Computes mean, median, and mode for numerical columns.
    visualize_data() -> None
        Creates a basic visualization of the data.
    export_statistics(file_path: str) -> None
        Exports the computed statistics to a CSV file.
    """

    def __init__(self):
        self.data: Optional[pd.DataFrame] = None
        self.statistics: Dict[str, Any] = {}

    def load_data(self, file_path: str) -> None:
        try:
            self.data = pd.read_csv(file_path)
            if self.data.empty:
                raise pd.errors.EmptyDataError("No columns to parse from file")
            self._validate_data()
            logging.info("Data loaded successfully.")
        except FileNotFoundError as e:
            logging.error("File not found. Please check the file path.")
            raise e
        except pd.errors.EmptyDataError as e:
            logging.error("No data. File is empty.")
            raise e
        except pd.errors.ParserError as e:
            logging.error("Error parsing data. Please check the file format.")
            raise e
        except Exception as e:
            logging.error(f"Unexpected error while loading data: {str(e)}")
            raise pd.errors.ParserError(f"Error parsing data: {str(e)}")

    def _validate_data(self) -> None:
        """
        Validate the loaded data.

        Raises
        ------
        ValueError
            If the data fails validation checks.
        """
        if self.data is None:
            raise ValueError("No data loaded.")
        if self.data.empty:
            raise ValueError("The loaded data is empty.")
        if self.data.isnull().all().all():
            raise ValueError("All values in the dataset are null.")

    def compute_statistics(self) -> None:
        """
        Compute mean, median, and mode for numerical columns in the dataset.

        Raises
        ------
        ValueError
            If no data is loaded or if there are no numerical columns.
        """
        if self.data is None:
            raise ValueError("No data to process. Please load data first.")

        try:
            numerical_data = self.data.select_dtypes(include=[np.number])
            if numerical_data.empty:
                raise ValueError("No numerical columns found in the dataset.")

            self.statistics = {
                'mean': self._compute_mean(numerical_data),
                'median': self._compute_median(numerical_data),
                'mode': self._compute_mode(numerical_data)
            }
            logging.info("Statistics computed successfully.")
        except Exception as e:
            logging.error(f"An error occurred while computing statistics: {e}")
            raise e

    def _compute_mean(self, data: pd.DataFrame) -> pd.Series:
        """
        Compute the mean of the numerical columns.

        Parameters
        ----------
        data : pd.DataFrame
            Data containing numerical columns.

        Returns
        -------
        pd.Series
            The mean of the numerical columns.
        """
        return data.mean()
    
    def _compute_mode(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Compute the mode of the numerical columns.

        Parameters
        ----------
        data : pd.DataFrame
            Data containing numerical columns.

        Returns
        -------
        pd.DataFrame
            The mode of the numerical columns.
        """
        return data.mode().iloc[0]  # Return the first mode if there are multiple

    def _compute_median(self, data: pd.DataFrame) -> pd.Series:
        """
        Compute the median of the numerical columns.

        Parameters
        ----------
        data : pd.DataFrame
            Data containing numerical columns.

        Returns
        -------
        pd.Series
            The median of the numerical columns.
        """
        return data.median()

    def _compute_mode(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Compute the mode of the numerical columns.

        Parameters
        ----------
        data : pd.DataFrame
            Data containing numerical columns.

        Returns
        -------
        pd.DataFrame
            The mode of the numerical columns.
        """
        return data.apply(lambda x: stats.mode(x)[0])

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get the computed statistics.

        Returns
        -------
        dict
            A dictionary containing mean, median, and mode for numerical columns.
        """
        return self.statistics

    def visualize_data(self, output_file: str = 'data_boxplot.png') -> None:
        """
        Create a basic visualization of the data and save it to a file.

        Parameters
        ----------
        output_file : str, optional
            The path where the plot will be saved (default is 'data_boxplot.png')

        Raises
        ------
        ValueError
            If no data is loaded or if there are no numerical columns.
        """
        if self.data is None:
            raise ValueError("No data to visualize. Please load data first.")
        
        try:
            numerical_data = self.data.select_dtypes(include=[np.number])
            if numerical_data.empty:
                raise ValueError("No numerical columns found in the dataset.")

            numerical_data.boxplot()
            plt.title('Boxplot of Numerical Data')
            plt.savefig(output_file)
            plt.close()  # Close the plot to free up memory
            logging.info(f"Data visualization saved as '{output_file}'.")
        except Exception as e:
            logging.error(f"An error occurred while visualizing data: {e}")
            raise e

    def export_statistics(self, file_path: str) -> None:
        """
        Export the computed statistics to a CSV file.

        Parameters
        ----------
        file_path : str
            The path where the CSV file will be saved.

        Raises
        ------
        ValueError
            If no statistics have been computed.
        """
        if not self.statistics:
            raise ValueError("No statistics to export. Please compute statistics first.")

        try:
            pd.DataFrame(self.statistics).to_csv(file_path)
            logging.info(f"Statistics exported successfully to {file_path}")
        except Exception as e:
            logging.error(f"An error occurred while exporting statistics: {e}")
            raise e

# Example Usage
if __name__ == "__main__":
    processor = DataProcessor()
    processor.load_data("data.csv")
    processor.compute_statistics()
    print(processor.get_statistics())
    processor.visualize_data()
    processor.export_statistics("statistics.csv")