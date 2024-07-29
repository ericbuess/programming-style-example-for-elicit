# Data Processor

This project provides a `DataProcessor` class for loading, processing, and analyzing data from CSV files. It includes functionality for computing basic statistics, visualizing data, and exporting results.

## Features

- Load data from CSV files
- Compute basic statistics (mean, median, mode) for numerical columns
- Visualize data using box plots
- Export computed statistics to CSV
- Comprehensive error handling and logging
- Unit tests for all major functionality

## Requirements

- Python 3.7+
- pandas
- numpy
- scipy
- matplotlib
- python-dotenv

## Project Structure

```plaintext
data-processor/
│
├── src/
│   ├── __init__.py
│   └── data_processor.py
│
├── tests/
│   ├── __init__.py
│   └── test_data_processor.py
│
├── data/
│   └── sample_data.csv
│
├── examples/
│   └── run_data_processor.py
│
├── output/  # Generated files will be saved here
│   ├── output_statistics.csv
│   └── data_boxplot.png
│
├── README.md
├── requirements.txt
├── .env
└── .gitignore
```

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/yourusername/data-processor.git
   cd data-processor
   ```

2. Set up a virtual environment (recommended):

   It's a best practice to create a virtual environment for your project. This keeps your project dependencies isolated from other projects and your system Python installation.

   If you're using conda, you can create a new environment with:

   ```
   conda create --name data-processor-env python=3.12
   conda activate data-processor-env
   ```

   Replace `3.12` with your preferred Python version that's compatible with the project requirements.

   If you prefer to use venv (Python's built-in virtual environment module), you can use:

   ```
   python -m venv data-processor-env
   source data-processor-env/bin/activate  # On Windows, use `data-processor-env\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Here's a basic example of how to use the `DataProcessor`:

```python
from src.data_processor import DataProcessor

processor = DataProcessor()
processor.load_data("data/sample_data.csv")
processor.compute_statistics()
print(processor.get_statistics())
processor.visualize_data()
processor.export_statistics("output/output_statistics.csv")
```

To run the example script with command-line arguments, navigate to the project root directory and run:

```bash
python examples/run_data_processor.py data/sample_data.csv --output output/my_stats.csv --plot output/my_plot.png
```

This command will:

1. Load the data from `data/sample_data.csv`
2. Compute and print the statistics
3. Create a visualization and save it as `output/my_plot.png`
4. Export the statistics to `output/my_stats.csv`

You can customize the input and output file paths as needed.

## Running Tests

To run the unit tests:

```bash
python -m unittest discover tests
```

## Configuration

You can set the log level using an environment variable. Create a `.env` file in the project root and add:

```
LOG_LEVEL=INFO
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Here are some ways you can contribute:

1. Report bugs or suggest features by opening an issue
2. Improve documentation
3. Add new functionality or improve existing code
4. Write additional tests to increase code coverage

When contributing, please:

1. Fork the repository and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. Ensure the test suite passes.
4. Make sure your code lints.
5. Issue that pull request!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Project Purpose

The Data Processor project aims to provide a simple yet flexible tool for data analysis and visualization. It's designed to be easily extendable and can serve as a starting point for more complex data processing tasks. Some potential use cases include:

1. Quick analysis of CSV datasets
2. Generating basic statistical reports
3. Creating visualizations for data exploration
4. As a educational tool for learning about data processing in Python

## Acknowledgments

- Thanks to all contributors who have helped improve this project.
- This project was inspired by the need for a simple, reusable data processing tool.

## Contact

If you have any questions or feedback, please open an issue on the GitHub repository.

Happy data processing!
