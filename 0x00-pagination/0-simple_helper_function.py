#!/usr/bin/env python3
"""Function that calculates the start and end index 
   for pagination based on page number and page size.
"""
from typing import Tuple

def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Given a page number and page size, return the start and end indexes
       for the records corresponding to that page.
    """
    start_index = (page - 1) * page_size
    end_index = page * page_size
    return start_index, end_index
