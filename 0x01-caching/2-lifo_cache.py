#!/usr/bin/env python3
"""Last-In First-Out (LIFO) caching system module."""

from collections import OrderedDict
from base_caching import BaseCaching

class LIFOCache(BaseCaching):
    """LIFO Caching system that inherits from BaseCaching.
    Implements Last-In, First-Out removal strategy when limit is reached.
    """
    
    def __init__(self):
        """Initialize LIFOCache with an ordered dictionary for caching."""
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Adds an item to the cache using LIFO policy.
        Discards the most recently added item when the cache limit is exceeded.
        
        Args:
            key (str): The key under which the item will be stored.
            item (any): The item to cache.
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                last_key, _ = self.cache_data.popitem(last=True)
                print("DISCARD:", last_key)
            self.cache_data[key] = item
            self.cache_data.move_to_end(key, last=True)

    def get(self, key):
        """Retrieves an item by key from the cache.
        
        Args:
            key (str): The key of the item to retrieve.
        
        Returns:
            The cached item if found, otherwise None.
        """
        return self.cache_data.get(key)

