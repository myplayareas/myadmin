import os
from flask import Flask
# register the database commands
from myapp.config import db
# apply the blueprints to the app
from myapp.control import auth
from myapp.control import dashboard
from myapp.control import usuario
from myapp.control import repositorio

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "myapp.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/sobre")
    def hello():
        return "Aplicacao Web Python usando Flask"

    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(usuario.bp)
    app.register_blueprint(repositorio.bp)

    # Define a rota principal da aplicacao
    app.add_url_rule("/", endpoint="index")

    return app