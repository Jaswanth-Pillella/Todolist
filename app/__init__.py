import os
from flask import Flask
from .controllers.todo_controller import todo_controller
from .controllers.theme_controller import theme_controller
from .controllers.user_controller import user_controller
from .middlewares.error_handler import setup_error_handler
from .middlewares.authentication_middleware import require_login_middleware
from .models import db
from .config import Config
from dotenv import load_dotenv
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Load config
    app.config.from_object(Config)

    # Set a secret key for session management
    app.secret_key = os.getenv("secret_key")

    # Initialize the database
    db.init_app(app)

    # Create database tables
    with app.app_context():
        db.create_all()

    # Setup error handler middleware
    setup_error_handler(app)

    # Setup authentication middleware
    require_login_middleware(app)

    # Register blueprints
    app.register_blueprint(todo_controller)
    app.register_blueprint(user_controller)
    app.register_blueprint(theme_controller)

    return app
