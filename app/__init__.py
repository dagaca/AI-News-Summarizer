"""
This module initializes the Flask application and sets up Swagger for API documentation.
"""
import os
from dotenv import load_dotenv
from flask import Flask
from flasgger import Swagger

# Load environment variables from .env file
load_dotenv()

# Create Flask application
app = Flask(__name__)

# Setting up Swagger configuration for API documentation
app.config['SWAGGER'] = {
    'title': 'AI News Summary API',
    'description': 'API for summarizing AI-related news using Hugging Face models.'
}

# Log directories configuration
app.config['LOG_DIR'] = os.getenv('LOG_DIR', 'logs')

# Create directories if they don't exist
os.makedirs(app.config['LOG_DIR'], exist_ok=True)

# Initialize Swagger
swagger = Swagger(app)

# Import log configuration and apply to the app
from config.log_config import configure_logging, log_request_info, log_response_info
configure_logging(app)
log_request_info(app)
log_response_info(app)

# Import and configure cache
from config.cache_config import configure_cache
configure_cache(app)

# Import routes at the end to avoid circular imports
from app import routes
