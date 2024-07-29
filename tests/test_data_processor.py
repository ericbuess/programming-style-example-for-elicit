import unittest
from src.data_processor import DataProcessor
import pandas as pd
import numpy as np
from unittest.mock import patch, mock_open
import os
import pytest

class TestDataProcessor(unittest.TestCase):

    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self.processor = DataProcessor()
        self.test_data = pd.DataFrame({
            'A': [1, 2, 2, 3],
            'B': [4, 4, 5, 6],
            'C': ['a', 'b', 'c', 'd']
        })
        self.processor.data = self.test_data

    def test_compute_statistics(self) -> None:
        """Test if statistics are computed correctly."""
        self.processor.compute_statistics()
        stats = self.processor.get_statistics()
        self.assertEqual(stats['mean']['A'], 2)
        self.assertEqual(stats['median']['B'], 4.5)
        self.assertEqual(stats['mode']['A'], 2)

    def test_load_data(self) -> None:
        """Test if data is loaded correctly from a CSV file."""
        with patch("builtins.open", mock_open(read_data="A,B,C\n1,4,a\n2,4,b\n2,5,c\n3,6,d")):
            self.processor.load_data("dummy_path.csv")
            self.assertIsNotNone(self.processor.data)

    def test_file_not_found(self) -> None:
        """Test if FileNotFoundError is raised for non-existent files."""
        with self.assertRaises(FileNotFoundError):
            self.processor.load_data("non_existent_file.csv")

    def test_empty_data(self) -> None:
        """Test if EmptyDataError is raised for empty files."""
        with patch("builtins.open", mock_open(read_data="")):
            with self.assertRaises(pd.errors.EmptyDataError):
                self.processor.load_data("empty.csv")

    def test_invalid_data(self) -> None:
        """Test if ParserError is raised for invalid data."""
        with patch("pandas.read_csv", side_effect=pd.errors.ParserError("Error parsing file")):
            with self.assertRaises(pd.errors.ParserError):
                self.processor.load_data("invalid.csv")

    def test_all_null_data(self) -> None:
        """Test if ValueError is raised for data with all null values."""
        with patch("pandas.read_csv", return_value=pd.DataFrame({'A': [None, None], 'B': [None, None]})):
            with self.assertRaises(ValueError):
                self.processor.load_data("all_null.csv")

    def test_visualize_data(self) -> None:
        """Test if visualization function is called with correct arguments."""
        with patch("matplotlib.pyplot.savefig") as mock_savefig:
            self.processor.visualize_data()
            mock_savefig.assert_called_once_with('data_boxplot.png')

    def test_export_statistics(self) -> None:
        """Test if statistics are exported correctly."""
        self.processor.compute_statistics()
        with patch("pandas.DataFrame.to_csv") as mock_to_csv:
            self.processor.export_statistics("test_stats.csv")
            mock_to_csv.assert_called_once_with("test_stats.csv")

    def test_export_statistics_no_data(self) -> None:
        """Test if ValueError is raised when exporting without computing statistics."""
        with self.assertRaises(ValueError):
            self.processor.export_statistics("test_stats.csv")

    def test_single_column_data(self) -> None:
        """Test if statistics are computed correctly for single column data."""
        self.processor.data = pd.DataFrame({'A': [1, 2, 3]})
        self.processor.compute_statistics()
        stats = self.processor.get_statistics()
        self.assertEqual(stats['mean']['A'], 2)
        self.assertEqual(stats['median']['A'], 2)
        self.assertEqual(stats['mode']['A'], 1)

    def test_single_row_data(self) -> None:
        """Test if statistics are computed correctly for single row data."""
        self.processor.data = pd.DataFrame({'A': [1], 'B': [2]})
        self.processor.compute_statistics()
        stats = self.processor.get_statistics()
        self.assertEqual(stats['mean']['A'], 1)
        self.assertEqual(stats['mean']['B'], 2)
        self.assertEqual(stats['median']['A'], 1)
        self.assertEqual(stats['median']['B'], 2)
        self.assertEqual(stats['mode']['A'], 1)
        self.assertEqual(stats['mode']['B'], 2)

@pytest.mark.parametrize("input_data, expected_mean", [
    (pd.DataFrame({'A': [1, 2, 3]}), {'A': 2}),
    (pd.DataFrame({'A': [1, 1, 1]}), {'A': 1}),
    (pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]}), {'A': 2, 'B': 5}),
])
def test_compute_mean(input_data, expected_mean):
    """Parametrized test for computing mean with various input data."""
    processor = DataProcessor()
    processor.data = input_data
    processor.compute_statistics()
    assert processor.get_statistics()['mean'].to_dict() == expected_mean

if __name__ == "__main__":
    unittest.main()