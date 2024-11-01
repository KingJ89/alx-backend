#!/usr/bin/env python3
"""Defines a BasicCache class that inherits from BaseCaching and is a simple caching system."""

from base_caching import BaseCaching

class BasicCache(BaseCaching):
    """Basic caching system that stores items without limit.
    Inherits from BaseCaching.
    """

    def put(self, key, item):
        """Assigns the item to the cache under the specified key.
        Args:
            key (str): The key under which to store the item.
            item (any): The item to store in the cache.
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """Retrieves an item by key from the cache.
        Args:
            key (str): The key of the item to retrieve.
        Returns:
            The item if it exists in the cache, otherwise None.
        """
        return self.cache_data.get(key)
