from flask import Flask
from NewsApp.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


# db.create_all()
# migrate = Migrate(app, db)

from NewsApp import models, views, stream_to_db
from NewsApp.stream_to_db import StreamToDb
csv_db_obj = StreamToDb()
csv_db_obj.stream_to_db()
