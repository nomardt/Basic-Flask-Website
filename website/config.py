import flask

def configure(app: flask.Flask) -> str:
    """Configures Flask object and return database name"""
    app.config['SESSION_TYPE'] = 'filesystem'

    db_name = 'database.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
    return db_name