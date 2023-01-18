import os
import flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import configure

db = SQLAlchemy()

def create_app() -> flask.Flask:
    """Initial setup"""
    app = flask.Flask(__name__)

    app.secret_key = 'KfVRbZZTJxMG5HaPT3KQWxKtYH67cUhcMsprxWWZp9EuMP84aj3PpcgBzDYf'

    db_name = configure(app)

    db.init_app(app)

    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app, db_name)

    login_manager = LoginManager()
    # Setting the page shown instead of page requiring log in
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app: flask.Flask, db_name: str) -> None:
    """Creates the database.db file"""
    if not os.path.exists('instance/' + db_name):
        with app.app_context():
            db.create_all()
            print("The db has been created!")