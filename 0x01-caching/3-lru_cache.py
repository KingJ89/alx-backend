#!/usr/bin/env python3
"""Least Recently Used (LRU) caching system module."""

from collections import OrderedDict
from base_caching import BaseCaching

class LRUCache(BaseCaching):
    """LRU Caching system that inherits from BaseCaching.
    Implements a Least Recently Used (LRU) eviction policy when the cache limit is exceeded.
    """

    def __init__(self):
        """Initialize LRUCache with an ordered dictionary for caching."""
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Adds an item to the cache using LRU policy.
        If the cache exceeds its limit, removes the least recently used item.
        
        Args:
            key (str): The key under which the item will be stored.
            item (any): The item to cache.
        """
        if key is not None and item 

