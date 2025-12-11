"""
Simple cache implementation
"""

class SimpleCache:
    """Simple in-memory cache"""
    
    def __init__(self):
        self._cache = {}
    
    def get(self, key):
        """Get value from cache"""
        return self._cache.get(key)
    
    def set(self, key, value, timeout=300):
        """Set value in cache"""
        self._cache[key] = value
        return True
    
    def delete(self, key):
        """Delete value from cache"""
        if key in self._cache:
            del self._cache[key]
            return True
        return False
    
    def clear(self):
        """Clear all cache"""
        self._cache.clear()

# Initialize cache
cache = SimpleCache()


def init_cache(app):
    """
    Initialize cache with Flask app
    
    Args:
        app: Flask application instance
    """
    return cache
