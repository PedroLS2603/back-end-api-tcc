from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('config.cfg')

    return app
       
app = create_app()
db = SQLAlchemy(app)
ma = Marshmallow(app)