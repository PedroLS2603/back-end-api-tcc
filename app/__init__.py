from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_pyfile('config.cfg')

    return app
       
app = create_app()
db = SQLAlchemy(app)
ma = Marshmallow(app)