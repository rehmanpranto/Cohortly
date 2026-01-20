"""
Main application entry point
"""
import os
import logging
from app import create_app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    app = create_app()
    logger.info("Application created successfully")
except Exception as e:
    logger.error(f"Failed to create application: {e}", exc_info=True)
    raise

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    logger.info(f"Starting application on port {port}, debug={debug}")
    app.run(host='0.0.0.0', port=port, debug=debug)
