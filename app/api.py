from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)

app.config.from_object(Config)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'development secret key'
db = SQLAlchemy(app)

print(db)

migrate = Migrate(app, db)

def _register_blueprint(blueprint, **options):
        app.register_blueprint(blueprint, **options)

from app.models import models
from app.routes import routes

_register_blueprint(routes._dicom_health)
_register_blueprint(routes._dicom_user)
_register_blueprint(routes._dicom_board)
_register_blueprint(routes._dicom_ticket)
_register_blueprint(routes._dicom_teams)
