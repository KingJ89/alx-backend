#!/usr/bin/env python3
"""Hypermedia pagination implementation.
    This module provides functionality for paginating a dataset 
    and retrieving hypermedia-like information.
"""
import csv
import math
from typing import Dict, List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Calculates the start and end indexes for pagination.
    
    Args:
        page (int): The current page number (1-indexed).
        page_size (int): The number of items per page.
    
    Returns:
        Tuple[int, int]: A tuple representing the start and end indexes.
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return start_index, end_index


class Server:
    """Server class to paginate a dataset of popular baby names.
    
    Attributes:
        DATA_FILE (str): Path to the CSV file containing the dataset.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initializes a new Server instance with dataset caching."""
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Loads and caches the dataset if not already cached.
        
        Returns:
            List[List]: A list of lists representing the dataset.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as file:
                reader = csv.reader(file)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Skip header

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Retrieves a specific page of the dataset.
        
        Args:
            page (int): The page number (1-indexed).
            page_size (int): The number of items per page.
        
        Returns:
            List[List]: A list of rows corresponding to the requested page.
        """
        assert isinstance(page, int) and isinstance(page_size, int), \
            "Page and page_size must be integers."
        assert page > 0 and page_size > 0, \
            "Page and page_size must be greater than zero."

        start_index, end_index = index_range(page, page_size)
        data = self.dataset()

        if start_index >= len(data):
            return []

        return data[start_index:end_index]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """Retrieves pagination details along with the data for a specific page.
        
        Args:
            page (int): The page number (1-indexed).
            page_size (int): The number of items per page.
        
        Returns:
            Dict: A dictionary with pagination metadata and page content.
        """
        data_page = self.get_page(page, page_size)
        start_index, end_index = index_range(page, page_size)
        total_data = len(self.dataset())
        total_pages = math.ceil(total_data / page_size)

        return {
            'page_size': len(data_page),
            'page': page,
            'data': data_page,
            'next_page': page + 1 if end_index < total_data else None,
            'prev_page': page - 1 if start_index > 0 else None,
            'total_pages': total_pages,
        }

