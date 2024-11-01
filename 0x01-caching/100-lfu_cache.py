#!/usr/bin/env python3
"""Least Frequently Used (LFU) Caching module."""

from collections import OrderedDict
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """LFUCache that inherits from BaseCaching.
    Implements a Least Frequently Used (LFU) caching eviction policy.
    """

    def __init__(self):
        """Initialize LFUCache with an ordered dictionary for caching and
        a frequency dictionary for tracking access counts.
        """
        super().__init__()
        self.cache_data = OrderedDict()
        self.freq = {}

    def __update_frequency(self, key):
        """Helper function to update the frequency of access for the given key."""
        if key in self.freq:
            self.freq[key] += 1
        else:
            self.freq[key] = 1
        # Reorder the cache based on frequency
        self.cache_data.move_to_end(key)

    def put(self, key, item):
        """Adds an item in the cache using LFU policy.
        If the cache exceeds its limit, removes the least frequently used item.
        
        Args:
            key (str): The key under which the item will be stored.
            item (any): The item to cache.
        """
        if key is None or item is None:
            return

        if key not in self.cache_data and len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            # Find and remove LFU item
            lfu_key = min(self.freq, key=self.freq.get)
            self.cache_data.pop(lfu_key)
            self.freq.pop(lfu_key)
            print("DISCARD:", lfu_key)

        # Insert or update item and adjust frequency
        self.cache_data[key] = item
        self.__update_frequency(key)

    def get(self, key):
        """Retrieves an item by key and updates its access frequency.
        
        Args:
            key (str): The key of the item to retrieve.
        
        Returns:
            The cached item if found, otherwise None.
        """
        if key in self.cache_data:
            self.__update_frequency(key)
            return self.cache_data[key]
        return None

