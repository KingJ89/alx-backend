#!/usr/bin/env python3
"""Least Recently Used (LRU) Caching module."""
from collections import OrderedDict
from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """LRUCache that inherits from BaseCaching and
       implements a caching system with an LRU eviction policy.
    """

    def __init__(self):
        """Initialize the LRUCache with an ordered dictionary for LRU tracking."""
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Add an item to the cache.
        
        If the cache exceeds the limit, evict the least recently used item.
        
        Args:
            key (str): The key under which the item will be stored.
            item (any): The item to cache.
        """
        if key is None or item is None:
            return

        # Remove least recently used item if cache exceeds limit
        if key not in self.cache_data and len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            lru_key, _ = self.cache_data.popitem(last=False)
            print("DISCARD:", lru_key)

        # Add or update the item and mark as most recently used
        self.cache_data[key] = item
        self.cache_data.move_to_end(key)

    def get(self, key):
        """Retrieve an item from the cache by key, updating its recent use.
        
        Args:
            key (str): The key of the item to retrieve.
        
        Returns:
            The cached item if found, otherwise None.
        """
        if key is not None and key in self.cache_data:
            # Mark the accessed key as most recently used
            self.cache_data.move_to_end(key)
            return self.cache_data[key]
        return None

