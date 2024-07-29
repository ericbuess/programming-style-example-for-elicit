import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_processor import DataProcessor
import argparse

def validate_file_path(file_path: str, should_exist: bool = True) -> str:
    """
    Validate the given file path.
    
    Args:
        file_path (str): The path to validate.
        should_exist (bool): Whether the file should already exist.
    
    Returns:
        str: The validated file path.
    
    Raises:
        argparse.ArgumentTypeError: If the path is invalid.
    """
    if should_exist and not os.path.exists(file_path):
        raise argparse.ArgumentTypeError(f"The file {file_path} does not exist")
    elif not should_exist:
        dir_path = os.path.dirname(file_path)
        if dir_path and not os.path.exists(dir_path):
            raise argparse.ArgumentTypeError(f"The directory {dir_path} does not exist")
    return file_path

def main():
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(description='Process data using DataProcessor')
    parser.add_argument('input_file', type=lambda x: validate_file_path(x, True), help='Input CSV file')
    parser.add_argument('--output', type=lambda x: validate_file_path(x, False), default='output/output_statistics.csv', help='Output statistics file')
    parser.add_argument('--plot', type=lambda x: validate_file_path(x, False), default='output/data_boxplot.png', help='Output plot file')
    args = parser.parse_args()

    # Initialize DataProcessor
    processor = DataProcessor()
    
    try:
        # Load data from input file
        processor.load_data(args.input_file)
        
        # Compute and display statistics
        processor.compute_statistics()
        print("Computed Statistics:")
        print(processor.get_statistics())
        
        # Generate and save visualization
        processor.visualize_data(args.plot)
        
        # Export statistics to file
        processor.export_statistics(args.output)
        
        print(f"\nData visualization saved as '{args.plot}'")
        print(f"Statistics exported to '{args.output}'")
    
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please make sure the CSV file exists in the specified path.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()