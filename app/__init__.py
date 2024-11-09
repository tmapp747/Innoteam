from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from flask_caching import Cache
from flask_wtf.csrf import CSRFProtect

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
limiter = Limiter(key_func=get_remote_address)
cache = Cache()
csrf = CSRFProtect()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(f'config.{config_name}')
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    CORS(app)
    cache.init_app(app)
    csrf.init_app(app)
    
    # Set up login configuration
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from app.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    from app.core import core_bp
    app.register_blueprint(core_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
