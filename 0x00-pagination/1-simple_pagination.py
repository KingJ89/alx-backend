#!/usr/bin/env python3
"""Simple pagination implementation.
    Includes a function to get index ranges for paginated data.
"""
import csv
from typing import List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Calculates the start and end indexes for pagination.
    
    Args:
        page (int): The current page number, starting from 1.
        page_size (int): The number of items per page.
    
    Returns:
        Tuple[int, int]: The start and end indexes for the page.
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return start_index, end_index


class Server:
    """Server class to paginate a dataset of popular baby names.
    
    Attributes:
        DATA_FILE (str): The file path to the CSV dataset.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initializes a new Server instance, with dataset caching."""
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Returns the cached dataset, loading it from the CSV file if necessary.
        
        Returns:
            List[List]: A list of lists representing the dataset.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as file:
                reader = csv.reader(file)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Skip the header row

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Retrieves a page of the dataset based on page number and page size.
        
        Args:
            page (int): The page number to retrieve (1-indexed).
            page_size (int): The number of items per page.
        
        Returns:
            List[List]: A list of rows corresponding to the requested page.
        """
        assert isinstance(page, int) and isinstance(page_size, int), \
            "Both page and page_size must be integers."
        assert page > 0 and page_size > 0, \
            "Page and page_size must be positive integers."

        start_index, end_index = index_range(page, page_size)
        data = self.dataset()
        
        if start_index >= len(data):
            return []

        return data[start_index:end_index]
