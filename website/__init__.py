import flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = flask.Flask(__name__)

    app.secret_key = 'KfVRbZZTJxMG5HaPT3KQWxKtYH67cUhcMsprxWWZp9EuMP84aj3PpcgBzDYf'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    # Setting the page shown instead of page requiring log in
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not os.path.exists('instance/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print("The db was created!")