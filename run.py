import os
from app import create_app
from flask.logging import create_logger
import logging
from logging.handlers import RotatingFileHandler

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.mkdir('logs')

# Configure logging
logging.basicConfig(level=logging.INFO)
file_handler = RotatingFileHandler(
    'logs/innoteam.log',
    maxBytes=10240,
    backupCount=10
)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)

# Create app instance
app = create_app(os.getenv('FLASK_CONFIG', 'default'))
logger = create_logger(app)
logger.addHandler(file_handler)

# Add logging to app
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Innoteam startup')

if __name__ == '__main__':
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    )
