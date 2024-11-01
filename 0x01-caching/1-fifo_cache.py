#!/usr/bin/env python3
"""FIFO caching inherits from BaseCaching
"""


from collections import OrderedDict

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """FIFOCache that inherits from BaseCaching
    """
    def __init__(self):
        """ cache initalization
        """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """adding item in cache
        """
        if key is None or item is None:
            return
        self.cache_data[key] = item
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            first_key, _ = self.cache_data.popitem(False)
            print("DISCARD:", first_key)

    def get(self, key):
        """ Return an Item by key
        """
        return self.cache_data.get(key, None)
