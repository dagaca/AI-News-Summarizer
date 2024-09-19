"""
This module provides caching configuration and initialization for the Flask application.
It sets up the caching mechanism using Flask-Caching, allowing the application to 
cache responses and reduce redundant processing.

The caching can be configured to use different backends like 'simple', 'redis', or 
'memcached', depending on the deployment environment. This module provides a simple 
cache setup that can be easily adjusted for more complex caching strategies.
"""

from flask_caching import Cache

# Create a Cache instance
cache = Cache()

def configure_cache(app):
    """
    Configures the caching settings for the Flask app.
    
    Args:
        app (Flask): The Flask application instance.
        
    The configuration sets the cache type and default timeout:
        - CACHE_TYPE: Defines the caching backend. The current setup uses 'simple',
          which stores the cache in memory, suitable for development or testing environments.
          This can be replaced with more robust options like 'redis' or 'memcached' for 
          production environments.
        - CACHE_DEFAULT_TIMEOUT: Specifies the default cache expiration time in seconds.
          The current setting is 300 seconds (5 minutes).
          
    The cache is initialized with the provided Flask app to enable caching of 
    routes, functions, or data as needed within the application.
    """
    # Define the cache configuration
    app.config['CACHE_TYPE'] = 'simple'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300

    # Initialize the cache with the app
    cache.init_app(app)
