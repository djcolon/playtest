"""File containing functions for loading test data."""

from csv import reader


def load_csv_data(path: str) -> list[tuple]:
    """Load csv data into memory."""
    with open(path, "r") as file:
        # Create csv reader object
        csv_reader = reader(file)

        # Skip the headers
        next(csv_reader)

        # Get all rows of the csv file as a list of tuples
        return list(map(tuple, csv_reader))
