from flask import Flask
from yourapp.config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from yourapp.errors import register_error_handlers

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    register_error_handlers(app)

    with app.app_context():
        from yourapp.blueprints.auth.routes import auth_bp
        from yourapp.blueprints.classes.routes import classes_bp
        from yourapp.blueprints.general.routes import general_bp
        app.register_blueprint(general_bp)
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(classes_bp, url_prefix='/classes')

    @login_manager.user_loader
    def load_user(user_id):
        from yourapp.models import User  # Import here to avoid circular imports
        return User.query.get(int(user_id))

    return app
