#!/usr/bin/env python3
"""Deletion-resilient hypermedia pagination
"""
import csv
from typing import Dict, List


class Server:
    """Server class to paginate a database of popular baby names.

    Attributes:
        DATA_FILE (str): Path to the dataset file.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initializes a new Server instance, with dataset and indexed dataset as None."""
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Loads the dataset from the CSV file if not already loaded.

        Returns:
            List[List]: The dataset, excluding the header row.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as file:
                reader = csv.reader(file)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Exclude header

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Creates and caches an indexed dataset, limited to the first 1000 entries.

        Returns:
            Dict[int, List]: A dictionary mapping each index to the corresponding data row.
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()[:1000]
            self.__indexed_dataset = {i: dataset[i] for i in range(len(dataset))}
        
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """Retrieves a page of data, starting from the given index and with a specified size.

        Args:
            index (int): The start index for retrieving the page.
            page_size (int): The number of records per page.

        Returns:
            Dict: A dictionary containing the current index, next index, page size, and page data.

        Raises:
            AssertionError: If the index is not valid or out of range.
        """
        data = self.indexed_dataset()
        assert index is not None and 0 <= index < len(data), "Invalid index"

        page_data = []
        current_index = index
        next_index = None

        while len(page_data) < page_size and current_index < len(data):
            page_data.append(data[current_index])
            current_index += 1

        # Set the next index if more data is available
        next_index = current_index if current_index < len(data) else None

        return {
            'index': index,
            'next_index': next_index,
            'page_size': len(page_data),
            'data': page_data,
        }

