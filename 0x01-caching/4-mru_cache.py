#!/usr/bin/env python3
"""Most Recently Used (MRU) Caching system module."""

from collections import OrderedDict
from base_caching import BaseCaching

class MRUCache(BaseCaching):
    """MRU Caching system that inherits from BaseCaching.
    Implements a Most Recently Used (MRU) eviction policy when the cache limit is reached.
    """

    def __init__(self):
        """Initialize MRUCache with an ordered dictionary for caching."""
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Adds an item to the cache using MRU policy.
        If the cache exceeds its limit, removes the most recently used item.
        
        Args:
            key (str): The key under which the item will be stored.
            item (any): The item to cache.
        """
        if key is not None and item is not None:
            # If cache is full, remove the most recently used item
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS and key not in self.cache_data:
                mru_key, _ = self.cache_data.popitem(last=False)
                print("DISCARD:", mru_key)
            # Add or update item and mark it as most recently used
            self.cache_data[key] = item
            self.cache_data.move_to_end(key, last=False)

    def get(self, key):
        """Retrieves an item by key and updates it as the most recently used.
        
        Args:
            key (str): The key of the item to retrieve.
        
        Returns:
            The cached item if found, otherwise None.
        """
        if key in self.cache_data:
            # Mark the item as most recently used
            self.cache_data.move_to_end(key, last=False)
            return self.cache_data[key]
        return None

