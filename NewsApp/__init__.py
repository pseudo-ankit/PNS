from flask import Flask
from NewsApp.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
# db.create_all()
# migrate = Migrate(app, db)

from NewsApp import views, models # , stream_to_db
